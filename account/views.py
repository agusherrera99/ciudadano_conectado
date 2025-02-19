from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import UserRegisterForm

# Create your views here.

def panel(request):
    return render(request, 'panel.html')

def profile(request):
    return render(request, 'profile.html')

def login_view(request):
    return render(request, 'registration/login.html')

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