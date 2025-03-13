from django.urls import path

from . import views


app_name = 'urban_management'

urlpatterns = [
    path('', views.urban_management, name='urban_management'),
    path('crear/', views.create_order, name='create_order'),
]