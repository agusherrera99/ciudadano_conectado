from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('panel/', views.panel, name='panel'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]