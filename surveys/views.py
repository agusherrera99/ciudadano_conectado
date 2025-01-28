from django.shortcuts import render

# Create your views here.

def surveys(request):
    return render(request, 'surveys.html')

def survey_detail(request, survey_id):
    return render(request, 'survey_detail.html')

def survey_results(request, survey_id):
    return render(request, 'survey_results.html')