from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('perfil/', views.profile, name='profile'),
    path('iniciar-sesion/', views.login_view, name='login'),
    path('registrarte/', views.register, name='register'),
]