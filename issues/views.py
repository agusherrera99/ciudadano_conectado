from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from .models import Issue, IssueUpdate

# Create your views here.

@login_required
def issues(request):
    issues = Issue.objects.filter(user=request.user)
    return render(request, 'issues.html', {'issues': issues})

@login_required
def issue_detail(request, issue_id):
    issue = Issue.objects.filter(user=request.user, id=issue_id).first()

    issue_updates = IssueUpdate.objects.filter(issue=issue
    ).order_by('updated_at')

    return render(request, 'issue_detail.html', {'issue': issue, 'issue_updates': issue_updates})

@login_required
def create_issue(request):
    if request.method == 'POST':
        try:
            issue = Issue.objects.create(
                category=request.POST['category'],
                description=request.POST['description'],
                user=request.user
            )
            issue.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid method'})