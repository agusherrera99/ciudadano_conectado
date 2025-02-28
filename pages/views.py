from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'

@login_required
def panel(request):
    return render(request, 'panel.html')

@login_required
def participation(request):
    return render(request, 'participation.html')

@login_required
def transparency(request):
    return render(request, 'transparency.html')

@login_required
def comunication(request):
    return render(request, 'comunication.html')