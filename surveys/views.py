from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from account.models import ExternalUser
from core.decorators import external_user_required
from .models import Answer, Survey, Question

# Create your views here.
@external_user_required
def surveys(request):
    # Actualizar estado de encuestas vencidas
    expired_surveys = Survey.objects.filter(
        status='activa',
        end_date__lt=timezone.now()
    )
    
    if expired_surveys.exists():
        expired_surveys.update(status='finalizada')
    
    surveys = Survey.objects.all()
    context = {
        'surveys': surveys,
        'url_link': reverse('pages:participation')
    }
    return render(request, 'surveys.html', context=context)

@external_user_required
def survey_detail(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    questions = Question.objects.filter(survey=survey).all()
    external_user = ExternalUser.objects.get(pk=request.user.id)
    already_answered = Answer.objects.filter(question__survey=survey, user=external_user).exists()

    context = {
        'survey': survey,
        'questions': questions,
        'already_answered': already_answered,
        'url_link': reverse('surveys:surveys')
    }
    return render(request, 'survey_detail.html', context=context)

@external_user_required
def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    questions = Question.objects.filter(survey=survey).prefetch_related('options')
    
    # Preparamos los datos en formato adecuado para JSON
    chart_data = {}
    results = []
    
    for question in questions:
        question_data = {
            'question': {
                'id': question.id,
                'text': question.question_text,
                'type': question.question_type
            },
            'total_answers': Answer.objects.filter(question=question).count()
        }
        
        # Preparamos los datos para las gráficas
        chart_item = {
            'type': question.question_type,
        }
        
        if question.question_type == 'predefinida':
            # Para preguntas predefinidas, procesamos las opciones
            options_data = []
            chart_options = []
            
            for option in question.options.all():
                option_count = Answer.objects.filter(
                    question=question,
                    answer_text=str(option.id)
                ).count()
                
                if question_data['total_answers'] > 0:
                    percentage = (option_count / question_data['total_answers']) * 100
                else:
                    percentage = 0
                
                option_item = {
                    'option': {
                        'id': option.id,
                        'option_text': option.option_text
                    },
                    'count': option_count,
                    'percentage': round(percentage, 1)
                }
                
                options_data.append(option_item)
                
                # Datos para el gráfico
                chart_options.append({
                    'name': option.option_text,
                    'value': option_count,
                    'percentage': round(percentage, 1)
                })
            
            question_data['options'] = options_data
            chart_item['options'] = chart_options
            
        else:
            # Para preguntas libres, obtenemos las respuestas textuales
            answers = list(Answer.objects.filter(question=question).values_list('answer_text', flat=True))
            question_data['answers'] = answers
            chart_item['answers'] = answers
        
        results.append(question_data)
        chart_data[f"question-{question.id}"] = chart_item
    
    context = {
        'survey': survey,
        'results': results,
        'chart_data': chart_data,
        'url_link': reverse('surveys:surveys')
    }
    
    return render(request, 'survey_results.html', context=context)

@external_user_required
def submit_survey(request, survey_id):
    is_external = request.user.is_external
    if not is_external:
        return JsonResponse({'status': False, 'error': 'No tienes permisos para realizar esta acción'})

    if request.method == 'POST':
        external_user = ExternalUser.objects.get(pk=request.user.id)
        if Answer.objects.filter(user=external_user, question__survey_id=survey_id).exists():
            return JsonResponse({'status': False, 'error': 'Ya has respondido esta encuesta'})
        
        try:
            survey = Survey.objects.get(pk=survey_id)
            
            questions = Question.objects.filter(survey=survey).all()
            for question in questions:
                answer_key = f'question-{question.id}'
                answer_text = request.POST.get(answer_key)
                
                # Guardar cada respuesta
                Answer.objects.create(
                    user=external_user,
                    question=question,
                    answer_text=answer_text
                )
            
            return JsonResponse({
                    'status': True,
                    'message': 'Encuesta enviada correctamente'
                })
        except Survey.DoesNotExist:
            return JsonResponse({'status': False, 'error': 'La encuesta no existe'})
        except Exception:
            return JsonResponse({'status': False, 'error': 'Error al enviar la encuesta'})
    else:
        return JsonResponse({'status': False, 'error': 'Método no permitido'})