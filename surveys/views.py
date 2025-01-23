from django.shortcuts import render

# Create your views here.


def survey_detail(request, survey_id):
    return render(request, 'survey_detail.html')

def survey_results(request, survey_id):
    return render(request, 'survey_results.html')