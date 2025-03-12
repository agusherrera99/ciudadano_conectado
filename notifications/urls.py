from django.urls import path

from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('marcar-como-leida/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
]