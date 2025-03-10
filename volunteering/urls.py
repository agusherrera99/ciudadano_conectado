from django.urls import path

from . import views

app_name = 'volunteering'

urlpatterns = [
    path('', views.volunteering, name='volunteering'),
]