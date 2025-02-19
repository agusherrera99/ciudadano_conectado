from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required
def issues(request):
    return render(request, 'issues.html')

@login_required
def issue_detail(request, issue_id):
    return render(request, 'issue_detail.html', {'issue_id': issue_id})