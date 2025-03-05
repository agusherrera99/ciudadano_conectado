from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse

from .models import Issue, IssueUpdate

# Create your views here.

@login_required
def issues(request):
    user_issues = Issue.objects.filter(user=request.user)
    issues = Issue.objects.all().order_by('-votes_count').exclude(user=request.user)[:5]

    context = {
        'user_issues': user_issues,
        'issues': issues,
        'url_link': reverse('pages:participation')
    }
    return render(request, 'issues.html', context=context)

@login_required
def issue_detail(request, issue_id):
    issue = Issue.objects.filter(user=request.user, id=issue_id).first()

    issue_updates = IssueUpdate.objects.filter(issue=issue
    ).order_by('updated_at')


    context = {
        'issue': issue,
        'issue_updates': issue_updates,
        'url_link': reverse('issues:issues')
    }
    return render(request, 'issue_detail.html', context=context)

@login_required
def create_issue(request):
    if request.method == 'POST':
        try:
            issue = Issue.objects.create(
                category=request.POST['category'],
                description=request.POST['description'],
                user=request.user,
                votes_count=1,
            )
            issue.votes.set([request.user])
            issue.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def vote_issue(request, issue_id):
    if request.method == 'POST':
        try:
            issue = Issue.objects.get(id=issue_id)
            action = request.POST.get('action')

            if action == 'up':
                issue.add_vote(request.user)
            elif action == 'down':
                issue.remove_vote(request.user)

            issue.refresh_from_db()
            votes_count = issue.votes_count

            return JsonResponse({
                'success': True,
                'votes': votes_count
            })
        except Issue.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Solicitud no encontrada'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
        
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })

