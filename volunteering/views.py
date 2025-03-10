from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count

from .models import Volunteer, Volunteering, VolunteerCategory
# Create your views here.

@login_required
def volunteering(request):
    # Obtener voluntariados con conteo de inscripciones
    volunteerings = Volunteering.objects.annotate(
        enrollment_count=Count('volunteer')
    ).all()
    categories = VolunteerCategory.objects.all()
    
    # Obtener todos los voluntariados en los que el usuario ya está inscrito
    user_volunteerings = Volunteer.objects.filter(user=request.user).values_list('volunteering_id', flat=True)
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

@login_required
def apply_volunteering(request):
    if request.method == 'POST':
        try:
            volunteering_id = request.POST.get('volunteering_id')
            if not volunteering_id:
                return JsonResponse({'status': 'error', 'message': 'No se seleccionó una oportunidad de voluntariado'})
                
            volunteering = Volunteering.objects.get(pk=volunteering_id)
            
            # Obtener disponibilidad como una lista
            availability_values = request.POST.getlist('availability')
            availability_str = '-'.join(availability_values)

            volunteer = Volunteer.objects.create(
                user=request.user,
                volunteering=volunteering,
                availability=availability_str,
                skills=request.POST.get('skills', ''),
                motivation=request.POST.get('motivation', ''),
            )
            volunteer.save()   
                    
            return JsonResponse({'status': 'success'})
        except Volunteering.DoesNotExist:
            return JsonResponse({'status': 'error'})
        except Exception:
            return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'error'})