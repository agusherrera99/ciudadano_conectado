from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import Volunteering
# Create your views here.

@login_required
def volunteering(request):
    volunteerings = Volunteering.objects.all()
    context = {
        'url_link': reverse('pages:participation'),
        'volunteerings': volunteerings
    }
    return render(request, 'volunteering.html', context=context)