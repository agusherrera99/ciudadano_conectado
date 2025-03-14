from django.db import models
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count

from account.models import ExternalUser
from core.decorators import external_user_required
from .models import Volunteer, Volunteering, VolunteerCategory
# Create your views here.

@external_user_required
def volunteering(request):
    # Obtener voluntariados con conteo de inscripciones
    volunteerings = Volunteering.objects.annotate(
        enrollment_count=Count('volunteer')
    ).all()
    categories = VolunteerCategory.objects.all()
    
    # Obtener todos los voluntariados en los que el usuario ya está inscrito
    external_user = ExternalUser.objects.get(id=request.user.id)
    user_volunteerings = Volunteer.objects.filter(user=external_user).values_list('volunteering_id', flat=True)
    already_volunteered = user_volunteerings.exists()

    enrollment_counts = Volunteer.objects.values('volunteering').annotate(count=models.Count('volunteering'))

    context = {
        'url_link': reverse('pages:participation'),
        'volunteerings': volunteerings,
        'already_volunteered': already_volunteered,
        'user_volunteerings': list(user_volunteerings),
        'enrollment_counts': enrollment_counts,
        'categories': categories,
    }
    return render(request, 'volunteering.html', context=context)

@external_user_required
def apply_volunteering(request):
    is_external = request.user.is_external
    if not is_external:
        return JsonResponse({'status': False, 'message': 'No tienes permisos para realizar esta acción'})
    
    if request.method == 'POST':
        try:
            volunteering_id = request.POST.get('volunteering_id')
            if not volunteering_id:
                return JsonResponse({'status': False, 'message': 'No se seleccionó una oportunidad de voluntariado'})
                
            volunteering = Volunteering.objects.get(pk=volunteering_id)
            
            # Obtener disponibilidad como una lista
            availability_values = request.POST.getlist('availability')
            availability_str = '-'.join(availability_values)

            external_user = ExternalUser.objects.get(id=request.user.id)
            volunteer = Volunteer.objects.create(
                user=external_user,
                volunteering=volunteering,
                availability=availability_str,
                skills=request.POST.get('skills', ''),
                motivation=request.POST.get('motivation', ''),
            )
            volunteer.save()   
                    
            return JsonResponse({'status': True})
        except Volunteering.DoesNotExist:
            return JsonResponse({'status': False})
        except Exception:
            return JsonResponse({'status': False})
    else:
        return JsonResponse({'status': False})