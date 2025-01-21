from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    # path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]