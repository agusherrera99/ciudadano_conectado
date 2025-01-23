from django.shortcuts import render

# Create your views here.

def issue_detail(request, issue_id):
    return render(request, 'issue_detail.html', {'issue_id': issue_id})