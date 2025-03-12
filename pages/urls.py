from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('panel/', views.panel, name='panel'),
    path('participacion/', views.participation, name='participation'),
    path('transparencia/', views.transparency, name='transparency'),
    path('comunicacion/', views.comunication, name='comunication'),
]