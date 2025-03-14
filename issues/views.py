from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from account.models import ExternalUser
from core.decorators import external_user_required
from .models import Issue, IssueUpdate

# Create your views here.

@external_user_required
def issues(request):
    user_issues = Issue.objects.filter(user=request.user)
    issues = Issue.objects.all().order_by('-votes_count').exclude(user=request.user)[:5]

    context = {
        'user_issues': user_issues,
        'issues': issues,
        'url_link': reverse('pages:participation')
    }
    return render(request, 'issues.html', context=context)

@external_user_required
def issue_detail(request, issue_id):
    issue = Issue.objects.filter(user=request.user, id=issue_id).first()

    issue_updates = IssueUpdate.objects.filter(issue=issue
    ).order_by('updated_at')


    context = {
        'issue': issue,
        'issue_updates': issue_updates,
        'url_link': reverse('issues:issues')
    }

    if issue.address:
        issue_address = issue.address.split(',')[:2]
        issue_address = ' '.join(issue_address)
        context['issue_address'] = issue_address

    return render(request, 'issue_detail.html', context=context)

@external_user_required
def create_issue(request):
    is_external = request.user.is_external
    if not is_external:
        return JsonResponse({'status': False, 'error': 'No tienes permisos para realizar esta acción'}, status=403)
    
    if request.method == 'POST':
        external_user = ExternalUser.objects.get(id=request.user.id)
        try:
            issue = Issue.objects.create(
                category=request.POST['category'],
                description=request.POST['description'],
                user=external_user,
                votes_count=1,
            )
            
            # Guardar ubicación si es un reclamo
            if issue.category == 'reclamo' and 'latitude' in request.POST and 'longitude' in request.POST:
                issue.latitude = request.POST.get('latitude')
                issue.longitude = request.POST.get('longitude')
                issue.address = request.POST.get('address', '')
                
            issue.votes.set([external_user])
            issue.save()
            return JsonResponse({'status': True})
        except Exception as e:
            return JsonResponse({'status': False, 'error': str(e)})
    return JsonResponse({'status': False, 'error': 'Método no permitido'})

@external_user_required
def vote_issue(request, issue_id):
    is_external = request.user.is_external
    if not is_external:
        return JsonResponse({'status': False, 'error': 'No tienes permisos para realizar esta acción'}, status=403)
    
    if request.method == 'POST':
        try:
            external_user = ExternalUser.objects.get(id=request.user.id)

            issue = Issue.objects.get(id=issue_id)
            action = request.POST.get('action')

            if action == 'up':
                issue.add_vote(external_user)
            elif action == 'down':
                issue.remove_vote(external_user)

            issue.refresh_from_db()
            votes_count = issue.votes_count

            return JsonResponse({
                'status': True,
                'votes': votes_count
            })
        except Issue.DoesNotExist:
            return JsonResponse({
                'status': False,
                'error': 'Solicitud no encontrada'
            })
        except Exception as e:
            return JsonResponse({
                'status': False,
                'error': str(e)
            })
        
    return JsonResponse({
        'status': False,
        'error': 'Método no permitido'
    })

