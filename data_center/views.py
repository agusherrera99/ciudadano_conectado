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
    """
    Genera datos de muestra según la categoría y el período.
    Si period='fulldata', devuelve el conjunto completo de datos.
    """
    # Generamos datos para los últimos 5 años, con datos mensuales
    end_date = datetime.now()
    start_date = datetime(end_date.year - 5, end_date.month, 1)
    
    # Generamos el conjunto completo de datos mensuales para 5 años
    full_labels = []
    full_values = []
    
    # Crear datos para cada mes
    current_date = start_date
    while current_date <= end_date:
        full_labels.append(current_date.strftime('%b %Y'))
        
        # Diferentes rangos de valores según la categoría para mantener coherencia
        if category == 'edad-y-sexo':
            full_values.append(random.randint(10, 100))
        elif category == 'educación':
            full_values.append(random.randint(50, 200))
        else:
            full_values.append(random.randint(10, 100))
            
        # Avanzar al siguiente mes
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)
    
    # Si se solicita el conjunto completo, lo devolvemos con datos para todos los períodos
    if period == 'fulldata':
        # Datos específicos para categorías
        if category == 'edad-y-sexo':
            # Para edad-y-sexo, usamos grupos de edad pero con valores que cambian en el tiempo
            age_groups = ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+']
            
            # Generar datos específicos para cada período
            monthly_labels = age_groups
            monthly_values = [random.randint(10, 100) for _ in range(len(age_groups))]
            
            quarterly_labels = age_groups
            quarterly_values = [random.randint(10, 100) for _ in range(len(age_groups))]
            
            yearly_labels = age_groups
            yearly_values = [random.randint(10, 100) for _ in range(len(age_groups))]
            
            five_year_labels = age_groups
            five_year_values = [random.randint(10, 100) for _ in range(len(age_groups))]
            
            title = 'Distribución por grupos de edad'
            
        elif category == 'educación':
            # Para educación, usamos niveles educativos pero con valores que cambian en el tiempo
            edu_levels = ['Primaria', 'Secundaria', 'Terciaria', 'Universitaria', 'Posgrado']
            
            # Generar datos específicos para cada período
            monthly_labels = edu_levels
            monthly_values = [random.randint(50, 200) for _ in range(len(edu_levels))]
            
            quarterly_labels = edu_levels
            quarterly_values = [random.randint(50, 200) for _ in range(len(edu_levels))]
            
            yearly_labels = edu_levels
            yearly_values = [random.randint(50, 200) for _ in range(len(edu_levels))]
            
            five_year_labels = edu_levels
            five_year_values = [random.randint(50, 200) for _ in range(len(edu_levels))]
            
            title = 'Nivel educativo de la población'
            
        else:
            # Para categorías standard, usamos datos temporales normales
            
            # Datos mensuales (últimos 6 puntos, cada 5 días)
            monthly_labels = []
            monthly_values = []
            for i in range(6):
                day = end_date - timedelta(days=(30 - i*5))
                monthly_labels.append(day.strftime('%d %b'))
                monthly_values.append(random.randint(10, 100))

            # Datos trimestrales (6 puntos, 2 por mes para los últimos 3 meses)
            quarterly_labels = []
            quarterly_values = []
            for i in range(3):
                month = end_date - timedelta(days=90 - i*30)
                quarterly_labels.append(month.strftime('%d %b'))
                quarterly_values.append(random.randint(10, 100))
                
                mid_month = end_date - timedelta(days=90 - (i*30 + 15))
                quarterly_labels.append(mid_month.strftime('%d %b'))
                quarterly_values.append(random.randint(10, 100))

            # Datos anuales (12 meses)
            yearly_labels = full_labels[-12:]
            yearly_values = full_values[-12:]
            
            title = f'Datos de {category.replace("-", " ").title()}'
        
        # Datos quinquenales (5 años)
        if category not in ['edad-y-sexo', 'educación']:
            five_year_labels = []
            five_year_values = []
            
            # Agrupar por año y obtener promedios
            for year in range(end_date.year - 4, end_date.year + 1):
                year_values = []
                for i, label in enumerate(full_labels):
                    if str(year) in label:
                        year_values.append(full_values[i])
                
                if year_values:
                    five_year_values.append(sum(year_values) // len(year_values))
                    five_year_labels.append(str(year))

        description = f'Información histórica sobre {category.replace("-", " ")}.'

        return {
            'title': title,
            'description': description,
            'monthly_labels': monthly_labels,
            'monthly_values': monthly_values,
            'quarterly_labels': quarterly_labels,
            'quarterly_values': quarterly_values,
            'yearly_labels': yearly_labels,
            'yearly_values': yearly_values,
            'five_year_labels': five_year_labels,
            'five_year_values': five_year_values
        }
    
    # Para solicitudes específicas de período (no fulldata)
    labels = []
    values = []
    
    # Generación de datos específicos según la categoría
    if category == 'edad-y-sexo':
        # Usamos grupos de edad pero con valores que cambian según el período
        age_groups = ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+']
        labels = age_groups
        values = [random.randint(10, 100) for _ in range(len(age_groups))]
        title = 'Distribución por grupos de edad'
        
    elif category == 'educación':
        # Usamos niveles educativos pero con valores que cambian según el período
        edu_levels = ['Primaria', 'Secundaria', 'Terciaria', 'Universitaria', 'Posgrado']
        labels = edu_levels
        values = [random.randint(50, 200) for _ in range(len(edu_levels))]
        title = 'Nivel educativo de la población'
        
    else:
        # Para categorías estándar, filtramos según el período solicitado
        if period == 'month':
            # Último mes (últimos 6 puntos, cada 5 días)
            for i in range(6):
                day = end_date - timedelta(days=(30 - i*5))
                labels.append(day.strftime('%d %b'))
                values.append(random.randint(10, 100))
            
        elif period == 'quarter':
            # Último trimestre (últimos 3 meses, 2 puntos por mes)
            for i in range(3):
                month = end_date - timedelta(days=90 - i*30)
                labels.append(month.strftime('%d %b'))
                values.append(random.randint(10, 100))
                
                mid_month = end_date - timedelta(days=90 - (i*30 + 15))
                labels.append(mid_month.strftime('%d %b'))
                values.append(random.randint(10, 100))
            
        elif period == 'year':
            # Último año (12 meses)
            labels = full_labels[-12:]
            values = full_values[-12:]
            
        else:  # '5years'
            # Para 5 años, agrupamos por año y calculamos promedios
            for year in range(end_date.year - 4, end_date.year + 1):
                year_values = []
                for i, label in enumerate(full_labels):
                    if str(year) in label:
                        year_values.append(full_values[i])
                
                if year_values:
                    values.append(sum(year_values) // len(year_values))
                    labels.append(str(year))
        
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