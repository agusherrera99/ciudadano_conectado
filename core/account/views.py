from django.shortcuts import render

# Create your views here.

def profile(request):
    return render(request, 'account/profile.html')

def login(request):
    return render(request, 'registration/login.html')

def register(request):
    return render(request, 'registration/register.html')