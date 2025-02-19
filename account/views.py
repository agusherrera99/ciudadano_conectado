from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from account.models import CustomUser

from .forms import UserLoginForm, UserRegisterForm

# Create your views here.

@login_required
def panel(request):
    return render(request, 'panel.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

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
                    messages.success(request, 'Login successful')
                    return redirect('account:panel')
            else:
                try:
                    user = CustomUser.objects.get(email=email)

                    if not user.is_active:
                        messages.error(request, 'Inactive user')
                    else:
                        messages.error(request, 'Invalid email or password')
                except CustomUser.DoesNotExist:
                    messages.error(request, 'This email is not registered')
        else:
            messages.error(request, 'Form is not valid')
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
                messages.success(request, 'Account created successfully')

                login(request, user)

                return redirect('account:panel')
            except Exception as e:
                messages.error(request, f'Error creating account: {e}')
        else:
            messages.error(request, 'Error creating account')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})