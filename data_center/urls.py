from django.urls import path

from . import views

app_name = 'data_center'

urlpatterns = [
    path('', views.data_center, name='data_center'),
    path('areas/', views.areas, name='areas'),
]