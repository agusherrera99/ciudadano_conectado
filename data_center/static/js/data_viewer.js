// Elementos DOM
const dataGroupSelect = document.getElementById('data-group');
const chartTypeSelect = document.getElementById('chart-type');
const timePeriodSelect = document.getElementById('time-period');
const loadingSpinner = document.getElementById('loading-spinner');

let dataChart = null;
let currentCategory = '';
let dataSet = null;

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
                dataChart.options.plugins.tooltip.callbacks.title = function (tooltipItems) {
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
    dataChart.options.plugins.title.text = data.title || `Datos de ${currentCategory.split('-').join(' ')}`;

    dataChart.update();
}

function processData(selectedGroup, selectedPeriod) {
    // Verificar si tenemos los datos necesarios
    if (!dataSet.data) {
        console.error('No hay datos disponibles');
        return;
    }

    // Preparar objeto de datos procesados
    const processedData = {
        labels: [],
        values: [],
        title: ''
    };

    // Obtener el grupo de datos seleccionado
    const groupData = dataSet.data.find(group => group.title === selectedGroup);
    if (!groupData) {
        console.error(`Grupo de datos "${selectedGroup}" no encontrado`);
        return;
    }

    // Asignar título del grupo de datos
    processedData.title = groupData.description

    // Procesar según el período seleccionado
    if (selectedPeriod === 'month') {
        // Usar los datos mensuales si están disponibles
        if (groupData.monthly_labels && groupData.monthly_values) {
            processedData.labels = [...groupData.monthly_labels];
            processedData.values = [...groupData.monthly_values];
        } else {
            console.warn('No hay datos mensuales disponibles.');
        }
    }
    else if (selectedPeriod === 'quarter') {
        // Usar los datos trimestrales si están disponibles
        if (groupData.quarterly_labels && groupData.quarterly_values) {
            processedData.labels = [...groupData.quarterly_labels];
            processedData.values = [...groupData.quarterly_values];
        } else {
            console.warn('No hay datos trimestrales disponibles.');
        }
    }
    else if (selectedPeriod === 'year') {
        // Usar los datos anuales
        if (groupData.yearly_labels && groupData.yearly_values) {
            processedData.labels = [...groupData.yearly_labels];
            processedData.values = [...groupData.yearly_values];
        } else {
            console.warn('No hay datos anuales disponibles.');

        }
    }
    else if (selectedPeriod === '5years') {
        // Usar los datos quinquenales
        if (groupData.five_year_labels && groupData.five_year_values) {
            processedData.labels = [...groupData.five_year_labels];
            processedData.values = [...groupData.five_year_values];
        } else {
            console.warn('No hay datos quinquenales disponibles.');

        }
    }

    // Ocultar indicador de carga
    loadingSpinner.style.display = 'none';

    // Actualizar la gráfica con los datos procesados
    updateChartData(processedData);
}

function fetchData() {
    // Mostrar indicador de carga
    loadingSpinner.style.display = 'flex';

    // Solicitar los datos completos (5 años)
    const apiUrl = `/centro-de-datos/api/data/?category=${currentCategory}`;

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
        dataSet = data;

        dataGroupSelect.innerHTML = ''; // Limpiar opciones previas
        // Llenar el select con las categorías disponibles
        dataSet.data.forEach(group => {
            const option = document.createElement('option');
            option.value = group.title;
            option.textContent = group.title;
            dataGroupSelect.appendChild(option);
        })

        // Procesar los datos según el período seleccionado
        processData(dataGroupSelect.value, timePeriodSelect.value);

        const indicators = document.getElementById('data-indicators');
        indicators.innerHTML = '';

        // Mostrar indicadores
        if (dataSet.indicators) {
            dataSet.indicators.forEach(indicator => {
                const indicatorDiv = document.createElement('div');
                indicatorDiv.className = 'indicator-item';
                indicatorDiv.innerHTML = `
                        <div class="indicator-header">
                            <strong>${indicator.label}:</strong>
                            <span class="indicator-value">${indicator.value}</span>
                        </div>
                        <p class="indicator-description">${indicator.description}</p>
                    `;
                indicators.appendChild(indicatorDiv);
            });
        } else {
            indicators.innerHTML = '<p>No hay indicadores disponibles para esta categoría.</p>';
        }
    })
    .catch(error => {
        console.error('Error al obtener datos:', error);
        // Ocultar indicador de carga
        loadingSpinner.style.display = 'none';

        // Mostrar mensaje de error
        /* document.getElementById('data-summary').innerHTML = `
            <div class="error-message">
                <p>Error: ${error.message}</p>
            </div>
        `; */
    });
}

function updateChart() {
    const chartType = chartTypeSelect.value;
    const timePeriod = timePeriodSelect.value;
    const selectedGroup = dataGroupSelect.value;

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
    if (dataSet) {
        processData(selectedGroup, timePeriod);
    } else {
        // Si no tenemos datos almacenados, solicitarlos
        fetchData();
    }
}

function initDataViewer(category) {
    currentCategory = category;

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
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
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
    dataGroupSelect.addEventListener('change', updateChart);
    chartTypeSelect.addEventListener('change', updateChart);
    timePeriodSelect.addEventListener('change', updateChart);

    // Carga inicial de datos completos
    fetchData();
}