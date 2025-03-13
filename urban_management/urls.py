from django.urls import path

from . import views


app_name = 'urban_management'

urlpatterns = [
    path('', views.urban_management, name='urban_management'),
]