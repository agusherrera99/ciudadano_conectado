from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


app_name = 'urban_management'

urlpatterns = [
    path('', views.urban_management, name='urban_management'),
    path('crear/', views.create_order, name='create_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)