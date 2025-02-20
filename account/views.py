from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import JsonResponse

from account.models import CustomUser

from .forms import UserLoginForm, UserRegisterForm, UserProfileForm

# Create your views here.

@login_required
def panel(request):
    return render(request, 'panel.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return JsonResponse({
                'success': True,
                'message': 'Perfil actualizado correctamente'
            })
        else:
            messages.error(request, 'Error al actualizar el perfil')
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Inicio de sesión correcto')
                    return redirect('account:panel')
            else:
                try:
                    user = CustomUser.objects.get(email=email)

                    if not user.is_active:
                        messages.error(request, 'Usuario inactivo')
                    else:
                        messages.error(request, 'Correo electrónico o contraseña incorrectos')
                except CustomUser.DoesNotExist:
                    messages.error(request, 'Este correo electrónico no está registrado')
        else:
            messages.error(request, 'Formulario inválido')
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                messages.success(request, 'Cuenta creada correctamente')

                login(request, user)

                return redirect('account:panel')
            except Exception:
                messages.error(request, 'Error al intentar crear la cuenta')
        else:
            messages.error(request, 'Error al intentar crear la cuenta')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})