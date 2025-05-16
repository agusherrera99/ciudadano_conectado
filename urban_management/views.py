from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from core.decorators import position_required
from urban_management.models import InternalUser, Ordering, OrderingManager

@position_required('inspector')
def urban_management(request):
    orderings = Ordering.objects.all().order_by('-priority', 'created_at')
    is_inspector = request.user.specific_instance.position.name == 'inspector'
    
    context = {
        'url_link': reverse('pages:panel'),
        'is_inspector': is_inspector,
        'orderings': orderings,
    }
    return render(request, 'urban_management.html', context=context)

@position_required('inspector')
def create_order(request):
    is_internal = request.user.is_internal
    if not is_internal:
        return JsonResponse({'status': False, 'message': 'No tienes permisos para realizar esta acción'}, status=403)
    
    is_inspector = request.user.specific_instance.position.name == 'inspector'
    if not is_inspector:
        return JsonResponse({'status': False, 'message': 'No tienes permisos para realizar esta acción'}, status=403)

    if request.method == 'POST':
        internal_user = request.user.specific_instance
        if not internal_user:
            return JsonResponse({'status': False, 'message': 'Usuario interno no encontrado'}, status=404)
        
        try:
            # Crear el ordenamiento primero
            ordering = Ordering.objects.create(
                category=request.POST['category'],
                description=request.POST['description'],
                latitude=request.POST.get('latitude'),
                longitude=request.POST.get('longitude'),
                address=request.POST.get('address', ''),
                inspector=internal_user,
            )
            
            # Buscar todos los gestores disponibles
            gestores = InternalUser.objects.filter(
                position__name='gestor',
                department__name='corralon_municipal'
            )
            
            # Asignar cada gestor al ordenamiento
            for gestor in gestores:
                OrderingManager.objects.create(
                    ordering=ordering,
                    manager=gestor
                )
            
            return JsonResponse({'status': True})
            
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
            
    return JsonResponse({'status': False, 'message': 'Método no permitido'})

@position_required('relevador')
def urban_management_relevador(request):
    orderings = Ordering.objects.all().order_by('-priority', 'created_at')
    is_relevador = request.user.specific_instance.position.name == 'relevador'
    
    context = {
        'url_link': reverse('pages:panel'),
        'is_relevador': is_relevador,
        'orderings': orderings,
    }
    return render(request, 'urban_management.html', context=context)

@position_required('relevador')
def create_order_relevador(request):
    is_internal = request.user.is_internal
    if not is_internal:
        return JsonResponse({'status': False, 'message': 'No tienes permisos para realizar esta acción'}, status=403)
    
    is_relevador = request.user.specific_instance.position.name == 'relevador'
    if not is_relevador:
        return JsonResponse({'status': False, 'message': 'No tienes permisos para realizar esta acción'}, status=403)

    if request.method == 'POST':
        internal_user = request.user.specific_instance
        if not internal_user:
            return JsonResponse({'status': False, 'message': 'Usuario interno no encontrado'}, status=404)
        
        try:
            # Crear el ordenamiento primero
            ordering = Ordering.objects.create(
                category=request.POST['category'],
                description=request.POST['description'],
                latitude=request.POST.get('latitude'),
                longitude=request.POST.get('longitude'),
                address=request.POST.get('address', ''),
                relevador=internal_user,
            )
            
            # Buscar todos los gestores disponibles
            gestores = InternalUser.objects.filter(
                position__name='gestor',
                department__name='corralon_municipal'
            )
            
            # Asignar cada gestor al ordenamiento
            for gestor in gestores:
                OrderingManager.objects.create(
                    ordering=ordering,
                    manager=gestor
                )
            
            return JsonResponse({'status': True})
            
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
            
    return JsonResponse({'status': False, 'message': 'Método no permitido'})