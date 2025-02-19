from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required
def surveys(request):
    return render(request, 'surveys.html')

@login_required
def survey_detail(request, survey_id):
    return render(request, 'survey_detail.html')

@login_required
def survey_results(request, survey_id):
    return render(request, 'survey_results.html')