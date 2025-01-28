from django.shortcuts import render

# Create your views here.

def issues(request):
    return render(request, 'issues.html')

def issue_detail(request, issue_id):
    return render(request, 'issue_detail.html', {'issue_id': issue_id})