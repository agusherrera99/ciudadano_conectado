from django.urls import path

from . import views

app_name = 'volunteering'

urlpatterns = [
    path('', views.volunteering, name='volunteering'),
    path('aplicar/', views.apply_volunteering, name='apply'),
]