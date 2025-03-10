from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Volunteer, Volunteering, VolunteerCategory
# Create your views here.

@login_required
def volunteering(request):
    volunteerings = Volunteering.objects.all()
    categories = VolunteerCategory.objects.all()

    context = {
        'url_link': reverse('pages:participation'),
        'volunteerings': volunteerings,
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
            availability_str = ','.join(availability_values)

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