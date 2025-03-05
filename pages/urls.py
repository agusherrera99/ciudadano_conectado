from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('panel/', views.panel, name='panel'),
    path('participation/', views.participation, name='participation'),
    path('transparency/', views.transparency, name='transparency'),
    path('comunication/', views.comunication, name='comunication'),
]