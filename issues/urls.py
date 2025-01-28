from django.urls import path

from . import views

app_name = 'issues'

urlpatterns = [
    path('', views.issues, name='issues'),
    path('<int:issue_id>/', views.issue_detail, name='issue_detail'),
]