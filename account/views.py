from django.shortcuts import render

# Create your views here.

def panel(request):
    return render(request, 'panel.html')

def profile(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'registration/login.html')

def register(request):
    return render(request, 'registration/register.html')