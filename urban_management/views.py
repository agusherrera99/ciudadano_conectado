from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from account.models import InternalUser
from core.decorators import internal_user_required
from urban_management.models import Ordering

# Create your views here.
def get_inspector_user(user):
    """
    Verifica si un usuario es un inspector interno.
    Retorna (internal_user, is_inspector)
    """
    internal_user = None
    is_inspector = False
    
    if user.is_authenticated:
        try:
            internal_user = InternalUser.objects.get(id=user.id)
            if internal_user.position and internal_user.position.name == 'inspector':
                is_inspector = True
        except InternalUser.DoesNotExist:
            pass
            
    return internal_user, is_inspector

@internal_user_required
def urban_management(request):
    orderings = Ordering.objects.all().order_by('-priority', 'created_at')
    internal_user, is_inspector = get_inspector_user(request.user)
    
    context = {
        'url_link': reverse('pages:panel'),
        'is_inspector': is_inspector,
        'orderings': orderings,
    }
    return render(request, 'urban_management.html', context=context)

def create_order(request):
    internal_user, is_inspector = get_inspector_user(request.user)

    if not is_inspector:
        return JsonResponse({'status': False, 'message': 'No tienes permisos para realizar esta acción'}, status=403)

    if request.method == 'POST':
        try:
            ordering = Ordering.objects.create(
                category=request.POST['category'],
                description=request.POST['description'],
                latitude=request.POST.get('latitude'),
                longitude=request.POST.get('longitude'),
                address=request.POST.get('address', ''),
                inspector=internal_user,
            )
                
            ordering.save()
            return JsonResponse({'status': True,})
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)})
    return JsonResponse({'status': False, 'message': 'Método no permitido'})