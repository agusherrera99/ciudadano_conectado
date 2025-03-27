"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuenta/', include('account.urls', namespace='account')),
    path('account/', include('django.contrib.auth.urls')),
    path('', include('pages.urls')),
    path('notificaciones/', include('notifications.urls', namespace='notifications')),
    path('solicitudes/', include('issues.urls', namespace='issues')),
    path('encuestas/', include('surveys.urls', namespace='surveys')),
    path('voluntariados/', include('volunteering.urls', namespace='volunteering')),
    path('ordenamientos-urbanos/', include('urban_management.urls', namespace='urban_management')),
    path('centro-de-datos/', include('data_center.urls', namespace='data_center')),
]
