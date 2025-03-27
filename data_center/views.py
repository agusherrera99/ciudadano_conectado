from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def data_center(request):
    context = {
        'url_link': reverse('pages:transparency')
    }
    return render(request, 'data_center.html', context=context)

def areas(request):
    context = {
        'url_link': reverse('data_center:data_center')
    }
    return render(request, 'areas.html', context=context)