from django.urls import path

from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('mark-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
]