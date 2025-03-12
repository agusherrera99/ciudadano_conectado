from django.urls import path

from . import views

app_name = 'surveys'

urlpatterns = [
    path('', views.surveys, name='surveys'),
    path('<int:survey_id>/', views.survey_detail, name='survey_detail'),
    path('<int:survey_id>/resultados/', views.survey_results, name='survey_results'),
    path('<int:survey_id>/enviar/', views.submit_survey, name='submit_survey'),
]