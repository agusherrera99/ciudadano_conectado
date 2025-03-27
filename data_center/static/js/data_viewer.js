let dataChart = null;
let currentCategory = '';

function initDataViewer(category) {
    currentCategory = category;
    
    // Elementos DOM
    const chartTypeSelect = document.getElementById('chart-type');
    const timePeriodSelect = document.getElementById('time-period');
    const loadingSpinner = document.getElementById('loading-spinner');
    
    // Inicialización del gráfico
    const ctx = document.getElementById('data-chart').getContext('2d');
    dataChart = new Chart(ctx, {
        type: 'bar',  // Tipo por defecto
        data: {
            labels: [],
            datasets: [{
                label: 'Datos',
                data: [],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                    'rgba(240, 128, 128, 0.6)',
                    'rgba(144, 238, 144, 0.6)',
                    'rgba(173, 216, 230, 0.6)',
                    'rgba(255, 192, 203, 0.6)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(240, 128, 128, 1)',
                    'rgba(144, 238, 144, 1)',
                    'rgba(173, 216, 230, 1)',
                    'rgba(255, 192, 203, 1)'
                ],
                borderWidth: 1,
                pointBackgroundColor: 'rgba(54, 162, 235, 0.8)',
                pointBorderColor: 'rgba(54, 162, 235, 1)',
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: {
                        // Auto-skip etiquetas cuando hay muchas
                        autoSkip: true,
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: `Datos de ${category || 'Categoría'}`
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            
                            // Manejar diferentes tipos de gráficos
                            if (dataChart.config.type === 'pie') {
                                // Para gráficos de pastel, el valor está directamente en parsed
                                const value = context.parsed;
                                const labelText = context.label || data.labels[context.dataIndex];
                                return `${labelText}: ${value} (${((value / context.dataset.data.reduce((a, b) => a + b, 0)) * 100).toFixed(1)}%)`;
                            } else if (dataChart.config.type === 'scatter') {
                                return `${label}: (${context.parsed.x}, ${context.parsed.y})`;
                            } else {
                                return `${label}: ${context.parsed.y}`;
                            }
                        }
                    }
                }
            }
        }
    });
    
    // Event listeners
    chartTypeSelect.addEventListener('change', updateChart);
    timePeriodSelect.addEventListener('change', updateChart);
    
    // Carga inicial de datos
    fetchData(timePeriodSelect.value);
    
    function updateChart() {
        const chartType = chartTypeSelect.value;
        const timePeriod = timePeriodSelect.value;
        
        // Actualizar tipo de gráfico
        dataChart.config.type = chartType;
        
        // Configuraciones específicas según tipo de gráfico
        if (chartType === 'pie') {
            dataChart.options.scales = {};
            dataChart.options.plugins.legend.display = true;
        } else if (chartType === 'scatter') {
            // Para gráficos de dispersión necesitamos actualizar la estructura de datos
            dataChart.options.scales = {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Valor X'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Valor Y'
                    }
                }
            };
            dataChart.options.plugins.legend.display = true;
        } else {
            dataChart.options.scales = {
                x: {
                    ticks: {
                        autoSkip: true,
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    beginAtZero: true
                }
            };
        }
        
        // Actualizar datos según el periodo seleccionado
        fetchData(timePeriod);
    }
    
    function fetchData(period) {
        // Mostrar indicador de carga
        loadingSpinner.style.display = 'flex';
        
        // URL de la API con los parámetros
        const apiUrl = `/centro-de-datos/api/data/?category=${currentCategory}&period=${period}`;
        
        // Petición AJAX
        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta de la red');
                }
                return response.json();
            })
            .then(data => {
                // Actualizar datos del gráfico
                updateChartData(data);
                
                // Ocultar indicador de carga
                loadingSpinner.style.display = 'none';
            })
            .catch(error => {
                console.error('Error al obtener datos:', error);
                // Ocultar indicador de carga
                loadingSpinner.style.display = 'none';
                
                // Mostrar mensaje de error
                document.getElementById('data-summary').innerHTML = `
                    <div class="error-message">
                        <p>Error: ${error.message}</p>
                    </div>
                `;
            });
    }
    
    function updateChartData(data) {
        const chartType = chartTypeSelect.value;

        // Verificar si hay muchas etiquetas para ajustar la visualización
        const hasManyLabels = data.labels && data.labels.length > 12;
        
        if (chartType === 'scatter') {
            // Para scatter plot, necesitamos transformar los datos a formato {x, y}
            const scatterData = [];
            for (let i = 0; i < data.values.length; i++) {
                scatterData.push({
                    x: i + 1, // Usamos índice+1 como valor X
                    y: data.values[i]
                });
            }
            dataChart.data.datasets[0].data = scatterData;
            // Scatter no usa etiquetas tradicionales
            dataChart.data.labels = [];
        } else {
            // Formato normal para otros tipos de gráficos
            dataChart.data.labels = data.labels;
            dataChart.data.datasets[0].data = data.values;

            // Si hay muchas etiquetas, dividir en múltiples datasets para mejor visualización
            if (hasManyLabels && (chartType === 'bar' || chartType === 'line')) {
                // Configurar para etiquetas más compactas
                dataChart.options.scales.x.ticks.autoSkip = true;
                dataChart.options.scales.x.ticks.maxTicksLimit = 12;
                
                // Mostrar leyenda cuando hay muchas etiquetas
                dataChart.options.plugins.legend.display = true;
                
                // Para gráfica de línea, añadir tooltip más detallado
                if (chartType === 'line') {
                    dataChart.options.plugins.tooltip.callbacks.title = function(tooltipItems) {
                        return data.labels[tooltipItems[0].dataIndex];
                    };
                }
            } else {
                // Para pocos datos, podemos ocultar la leyenda si no es circular
                if (chartType !== 'pie') {
                    dataChart.options.plugins.legend.display = false;
                }
            }
        }
        
        dataChart.data.datasets[0].label = data.title || 'Datos';
        dataChart.options.plugins.title.text = data.title || `Datos de ${currentCategory}`;
        
        // Actualizamos el resumen
        document.getElementById('data-summary').innerHTML = `
            <p>${data.description || 'No hay descripción disponible para estos datos.'}</p>
        `;
        
        dataChart.update();
    }
}