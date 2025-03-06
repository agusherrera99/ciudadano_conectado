from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import Survey
# Create your views here.

@login_required
def surveys(request):
    surveys = Survey.objects.all()
    context = {
        'surveys': surveys,
        'url_link': reverse('pages:participation')
    }
    return render(request, 'surveys.html', context=context)

@login_required
def survey_detail(request, survey_id):
    context = {
        'survey': Survey.objects.get(pk=survey_id),
        'url_link': reverse('surveys:surveys')
    }
    return render(request, 'survey_detail.html', context=context)

@login_required
def survey_results(request, survey_id):
    return render(request, 'survey_results.html')