from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('panel/', views.panel, name='panel'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
]