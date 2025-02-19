from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from .models import Issue

# Create your views here.

@login_required
def issues(request):
    issues = Issue.objects.filter(user=request.user)
    return render(request, 'issues.html', {'issues': issues})

@login_required
def issue_detail(request, issue_id):
    return render(request, 'issue_detail.html', {'issue_id': issue_id})

@login_required
def create_issue(request):
    if request.method == 'POST':
        try:
            issue = Issue.objects.create(
                title=request.POST['title'],
                category=request.POST['category'],
                description=request.POST['description'],
                user=request.user
            )
            issue.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid method'})