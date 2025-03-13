from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def urban_management(request):
    context = {
        'url_link': reverse('pages:panel')
    }
    return render(request, 'urban_management.html')