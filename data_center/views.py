import json
import random
import os

from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse


# Create your views here.
def data_center(request):
    context = {
        'url_link': reverse('pages:transparency')
    }
    return render(request, 'data_center.html', context=context)

def areas(request):
    areas_path = os.path.join(os.path.dirname(__file__), 'static', 'json', 'areas.json')
    with open(areas_path, 'r') as file:
        areas = json.load(file)
    areas = sorted(areas, key=lambda x: x['title'])
    
    context = {
        'areas': areas,
        'url_link': reverse('data_center:data_center')
    }
    return render(request, 'areas.html', context=context)

def data_viewer(request, category=None):
    title = 'Sin Categoria'
    if '-' in category:
        title = category.split('-')
        title = ' '.join([word.capitalize() if word != 'y' else word for word in title])
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
    
    # acá se obtendría la información de una base de datos
    try:
        data = generate_sample_data(category)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def generate_sample_data(category):
    """
    Genera datos de muestra según la categoría y el período.
    devuelve el conjunto completo de datos.
    """
    data = []
    indicators = []
    groups = []
    
    if category == 'edad-y-sexo':
        age_groups = {
            'title': 'edades',
            'description': 'Distribución por grupos de edad',
            'labels': ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+']
        }
        sex_groups = {
            'title': 'sexos',
            'description': 'Distribución por sexo',
            'labels': ['Masculino', 'Femenino']
        }

        groups = [age_groups, sex_groups]
        

        indicators = [
            {
                'label': 'Natalidad',
                'value': random.randint(100, 500),
                'description': 'Número de nacimientos en el último año',
            },
            {
                'label': 'Mortalidad',
                'value': random.randint(50, 300),
                'description': 'Número de muertes en el último año',
            },
            {
                'label': 'Esperanza de vida',
                'value': random.randint(70, 85),
                'description': 'Esperanza de vida al nacer',
            },
            {
                'label': 'Tasa de fecundidad',
                'value': f"{round(random.uniform(1.5, 3.0), 2)}%",
                'description': 'Número promedio de hijos por mujer',
            }
        ]
    elif category == 'educación':
        edu_group = {
            'title': 'educación',
            'description': 'Distribución por niveles educativos',
            'labels': ['Ninguno', 'Primaria', 'Secundaria', 'Preparatoria', 'Universidad']
        }
        groups = [edu_group]

        indicators = [
            {
                'label': 'Tasa de alfabetización',
                'value': f"{random.randint(80, 100)}%",
                'description': 'Porcentaje de personas alfabetizadas',
            },
            {
                'label': 'Tasa de graduación',
                'value': f"{random.randint(50, 100)}%",
                'description': 'Porcentaje de estudiantes que se gradúan',
            },
            {
                'label': 'Promedio de años de escolaridad',
                'value': random.randint(8, 16),
                'description': 'Promedio de años de escolaridad por persona',
            }
        ]   

    for group in groups:
        title = group.get('title')
        labels = group.get('labels')
        monthly_labels = quarterly_labels = yearly_labels = five_year_labels = labels
        description = group.get('description')
        
        monthly_values = [random.randint(10, 100) for _ in range(len(labels))]
        quarterly_values = [random.randint(10, 100) for _ in range(len(labels))]
        yearly_values = [random.randint(10, 100) for _ in range(len(labels))]
        five_year_values = [random.randint(10, 100) for _ in range(len(labels))]

        data.append({
            'title': title,
            'description': description,
            'monthly_labels': monthly_labels,
            'monthly_values': monthly_values,
            'quarterly_labels': quarterly_labels,
            'quarterly_values': quarterly_values,
            'yearly_labels': yearly_labels,
            'yearly_values': yearly_values,
            'five_year_labels': five_year_labels,
            'five_year_values': five_year_values,
        }) 

    return {
        'data': data,
        'indicators': indicators,
    }