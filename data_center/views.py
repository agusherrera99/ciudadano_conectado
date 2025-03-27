from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import random
from datetime import datetime, timedelta

# Create your views here.
def data_center(request):
    context = {
        'url_link': reverse('pages:transparency')
    }
    return render(request, 'data_center.html', context=context)

def areas(request):
    context = {
        'url_link': reverse('data_center:data_center')
    }
    return render(request, 'areas.html', context=context)

def data_viewer(request, category=None):
    title = 'Sin Categoria'
    if '-' in category:
        title = category.split('-')
        title = ' '.join([word.capitalize() for word in title if word != 'y'])
    else:
        title = category.capitalize()

    context = {
        'url_link': reverse('data_center:areas'),
        'category': category,
        'title': title,
    }
    return render(request, 'data_viewer.html', context=context)

def api_data(request):
    """API para obtener datos según la categoría y el período seleccionado"""
    category = request.GET.get('category', 'default')
    period = request.GET.get('period', 'year')
    
    # acá se obtendría la información de una base de datos
    data = generate_sample_data(category, period)
    
    return JsonResponse(data)

def generate_sample_data(category, period):
    """Genera datos de muestra según la categoría y el período"""
    labels = []
    values = []
    title = ""
    description = ""
    
    # Generación de fechas según el período
    end_date = datetime.now()
    
    if period == 'month':
        start_date = end_date - timedelta(days=30)
        step = 5  # Cada 5 días
    elif period == 'quarter':
        start_date = end_date - timedelta(days=90)
        step = 15  # Cada 15 días
    elif period == '5years':
        start_date = datetime(end_date.year - 5, 1, 1)
        step = 365  # Anual
    else:  # year (default)
        start_date = datetime(end_date.year - 1, end_date.month, 1)
        step = 30  # Mensual
    
    # Generación de datos específicos por categoría
    if category == 'edad-y-sexo':
        labels = ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+']
        if period == '5years' or period == 'year':
            values = [random.randint(10, 100) for _ in range(len(labels))]
            title = 'Distribución por grupos de edad'
            description = 'Muestra la distribución de la población por grupos de edad en el período seleccionado.'
        else:
            # Datos temporales para períodos más cortos
            current_date = start_date
            while current_date <= end_date:
                values.append(random.randint(10, 20))
                current_date += timedelta(days=step)
            
            title = 'Población por edad a lo largo del tiempo'
            description = f'Evolución de la distribución demográfica durante el último {period_to_text(period)}.'
    
    elif category == 'educación':
        labels = ['Primaria', 'Secundaria', 'Terciaria', 'Universitaria', 'Posgrado']
        if period == '5years' or period == 'year':
            values = [random.randint(50, 200) for _ in range(len(labels))]
            title = 'Nivel educativo de la población'
            description = 'Distribución de la población según su nivel educativo máximo alcanzado.'
        else:
            current_date = start_date
            while current_date <= end_date:
                values.append(random.randint(10, 30))
                current_date += timedelta(days=step)
            
            title = 'Estadísticas educativas'
            description = f'Datos sobre nivel educativo durante el último {period_to_text(period)}.'
    
    # Datos por defecto para otras categorías
    else:
        labels = ['Categoría 1', 'Categoría 2', 'Categoría 3', 'Categoría 4', 'Categoría 5']
        if period == '5years' or period == 'year':
            values = [random.randint(10, 100) for _ in range(len(labels))]
        else:
            current_date = start_date
            while current_date <= end_date:
                values.append(random.randint(10, 50))
                current_date += timedelta(days=step)
        
        title = f'Datos de {category.replace("-", " ").title()}'
        description = f'Información sobre {category.replace("-", " ")} durante el último {period_to_text(period)}.'
    
    return {
        'labels': labels,
        'values': values,
        'title': title,
        'description': description,
    }

def period_to_text(period):
    """Convierte el código de período a texto legible"""
    if period == 'month':
        return 'mes'
    elif period == 'quarter':
        return 'trimestre'
    elif period == '5years':
        return 'quinquenio'
    else:
        return 'año'