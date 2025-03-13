from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from urban_management.models import Ordering

# Create your views here.
def urban_management(request):
    orderings = Ordering.objects.all().order_by('-priority', 'created_at')
    
    context = {
        'url_link': reverse('pages:panel'),
        'orderings': orderings,
    }
    return render(request, 'urban_management.html', context=context)

def create_order(request):
    if request.method == 'POST':
        try:
            ordering = Ordering.objects.create(
                category=request.POST['category'],
                description=request.POST['description'],
                latitude=request.POST.get('latitude'),
                longitude=request.POST.get('longitude'),
                address=request.POST.get('address', ''),
            )
                
            ordering.save()
            return JsonResponse({'status': True,})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False, 'message': 'Método no permitido'})