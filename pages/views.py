from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'

@login_required
def panel(request):
    return render(request, 'panel.html')

@login_required
def participation(request):
    context = {
        'url_link': reverse('pages:panel')
    }
    return render(request, 'participation.html', context=context)

def transparency(request):
    context = {
        'url_link': reverse('pages:panel')
    }
    return render(request, 'transparency.html', context=context)

@login_required
def comunication(request):
    context = {
        'url_link': reverse('pages:panel')
    }
    return render(request, 'comunication.html', context=context)