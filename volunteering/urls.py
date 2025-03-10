from django.urls import path

from . import views

app_name = 'volunteering'

urlpatterns = [
    path('', views.volunteering, name='volunteering'),
    path('apply/', views.apply_volunteering, name='apply'),
]