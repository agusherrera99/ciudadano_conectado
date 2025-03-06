from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Answer, Survey, Question
# Create your views here.

@login_required
def surveys(request):
    surveys = Survey.objects.all()
    context = {
        'surveys': surveys,
        'url_link': reverse('pages:participation')
    }
    return render(request, 'surveys.html', context=context)

@login_required
def survey_detail(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    questions = Question.objects.filter(survey=survey).all()
    already_answered = Answer.objects.filter(question__survey=survey, user=request.user).exists()

    context = {
        'survey': survey,
        'questions': questions,
        'already_answered': already_answered,
        'url_link': reverse('surveys:surveys')
    }
    return render(request, 'survey_detail.html', context=context)

@login_required
def survey_results(request, survey_id):
    return render(request, 'survey_results.html')

@login_required
def submit_survey(request, survey_id):
    if request.method == 'POST':
        try:
            survey = Survey.objects.get(pk=survey_id)
            
            questions = Question.objects.filter(survey=survey).all()
            for question in questions:
                answer_key = f'question-{question.id}'
                answer_text = request.POST.get(answer_key)
                
                # Guardar cada respuesta
                Answer.objects.create(
                    user=request.user,
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