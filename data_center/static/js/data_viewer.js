let dataChart = null;
let currentCategory = '';
let fullDataSet = null; // Almacenará el conjunto completo de datos

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
                            if (dataChart.config.type === 'pie' || dataChart.config.type === 'doughnut') {
                                // Para gráficos de pastel
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${context.label}: ${value} (${percentage}%)`;
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
    
    // Carga inicial de datos completos
    fetchFullData();
    
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
        
        // Actualizar datos según el periodo seleccionado usando los datos almacenados
        if (fullDataSet) {
            processDataForPeriod(timePeriod);
        } else {
            // Si no tenemos datos almacenados, solicitarlos
            fetchFullData();
        }
    }
    
    function fetchFullData() {
        // Mostrar indicador de carga
        loadingSpinner.style.display = 'flex';
        
        // Solicitar los datos completos (5 años)
        const apiUrl = `/centro-de-datos/api/data/?category=${currentCategory}&period=fulldata`;
        
        // Petición AJAX
        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta de la red');
                }
                return response.json();
            })
            .then(data => {
                // Almacenar los datos completos
                fullDataSet = data;
                
                // Procesar los datos según el período seleccionado
                processDataForPeriod(timePeriodSelect.value);
                
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
    
    function processDataForPeriod(period) {
        // Verificar si tenemos los datos necesarios
        if (!fullDataSet) {
            console.error('No hay datos disponibles');
            return;
        }
        
        // Preparar objeto de datos procesados
        const processedData = {
            labels: [],
            values: [],
            title: fullDataSet.title || `Datos de ${currentCategory.replace('-', ' ')}`,
            description: `Información sobre ${currentCategory.replace('-', ' ')} durante el último ${periodToText(period)}.`
        };
        
        // Procesar según el período seleccionado
        if (period === 'month') {
            // Usar los datos mensuales si están disponibles
            if (fullDataSet.monthly_labels && fullDataSet.monthly_values) {
                processedData.labels = [...fullDataSet.monthly_labels];
                processedData.values = [...fullDataSet.monthly_values];
            } else {
                console.warn('No hay datos mensuales disponibles, generando datos temporales');
                // Generar datos de respaldo
                const today = new Date();
                for (let i = 0; i < 6; i++) {
                    const day = new Date(today);
                    day.setDate(today.getDate() - (30 - i*5));
                    processedData.labels.push(day.getDate() + ' ' + day.toLocaleString('es', { month: 'short' }));
                    // Usar datos aleatorios como respaldo
                    processedData.values.push(Math.floor(Math.random() * 90) + 10);
                }
            }
        } 
        else if (period === 'quarter') {
            // Usar los datos trimestrales si están disponibles
            if (fullDataSet.quarterly_labels && fullDataSet.quarterly_values) {
                processedData.labels = [...fullDataSet.quarterly_labels];
                processedData.values = [...fullDataSet.quarterly_values];
            } else {
                console.warn('No hay datos trimestrales disponibles, generando datos temporales');
                // Generar datos de respaldo
                const today = new Date();
                for (let i = 0; i < 3; i++) {
                    const month = new Date(today);
                    month.setMonth(today.getMonth() - (3 - i));
                    
                    // Primer punto del mes (día 1)
                    const dateStr1 = '01 ' + month.toLocaleString('es', { month: 'short' });
                    processedData.labels.push(dateStr1);
                    processedData.values.push(Math.floor(Math.random() * 90) + 10);
                    
                    // Segundo punto del mes (día 15)
                    const dateStr2 = '15 ' + month.toLocaleString('es', { month: 'short' });
                    processedData.labels.push(dateStr2);
                    processedData.values.push(Math.floor(Math.random() * 90) + 10);
                }
            }
        }
        else if (period === 'year') {
            // Usar los datos anuales
            if (fullDataSet.yearly_labels && fullDataSet.yearly_values) {
                processedData.labels = [...fullDataSet.yearly_labels];
                processedData.values = [...fullDataSet.yearly_values];
            } else {
                console.warn('No hay datos anuales disponibles');
                // Usar los datos disponibles si es posible
                if (fullDataSet.labels && fullDataSet.values) {
                    processedData.labels = [...fullDataSet.labels];
                    processedData.values = [...fullDataSet.values];
                }
            }
        }
        else if (period === '5years') {
            // Usar los datos quinquenales
            if (fullDataSet.five_year_labels && fullDataSet.five_year_values) {
                processedData.labels = [...fullDataSet.five_year_labels];
                processedData.values = [...fullDataSet.five_year_values];
            } else {
                console.warn('No hay datos quinquenales disponibles');
                // Usar datos de respaldo
                const currentYear = new Date().getFullYear();
                for (let i = 0; i < 5; i++) {
                    processedData.labels.push(String(currentYear - 4 + i));
                    processedData.values.push(Math.floor(Math.random() * 90) + 10);
                }
            }
        }
        
        // Actualizar la gráfica con los datos procesados
        updateChartData(processedData);
    }
    
    function periodToText(period) {
        switch (period) {
            case 'month': return 'mes';
            case 'quarter': return 'trimestre';
            case 'year': return 'año';
            case '5years': return 'quinquenio';
            default: return 'período';
        }
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

            // Si hay muchas etiquetas, ajustar visualización
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