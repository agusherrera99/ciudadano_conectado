document.addEventListener("DOMContentLoaded", function () {
    // Colores para los gráficos
    const chartColors = [
        '#4285F4', '#34A853', '#FBBC05', '#EA4335', 
        '#8AB4F8', '#1967D2', '#5BB974', '#F6C934',
        '#D2E3FC', '#CEEAD6', '#FEF7E0', '#FAD2CF'
    ];
    
    // Inicializar surveyData
    let surveyData;
    
    // Función principal asíncrona para cargar y procesar datos
    async function initCharts() {
        try {
            // Recuperamos los datos de forma segura desde el tag json_script
            const chartDataElement = document.getElementById('chart-data');
            if (!chartDataElement) {
                return;
            }
            
            // Parsear los datos de forma asíncrona
            surveyData = JSON.parse(chartDataElement.textContent);
            
            // Verificar si ECharts está cargado correctamente
            if (typeof echarts === 'undefined') {
                return;
            }
            
            // Creamos un array de promesas para todas las visualizaciones
            const chartPromises = [];
            
            // Procesar los datos y crear gráficos
            for (const [key, data] of Object.entries(surveyData)) {
                const questionId = key.split('-')[1];
                
                if (data.type === 'predefinida') {
                    // Añadir promesa para crear gráfico
                    chartPromises.push(
                        createChartAsync(questionId, data.options)
                    );
                } else {
                    // Añadir promesa para crear nube de palabras
                    chartPromises.push(
                        createWordCloudAsync(questionId, data.answers)
                    );
                }
            }
            
            // Esperar a que todas las visualizaciones se carguen, pero no bloquear si alguna falla
            await Promise.allSettled(chartPromises);
            
            // Quitar cualquier indicador de carga si existe
            document.querySelectorAll('.chart-loading').forEach(loader => {
                loader.style.display = 'none';
            });
            
        } catch (error) {
            // Asegurarse de que los indicadores de carga desaparezcan en caso de error
            document.querySelectorAll('.chart-loading').forEach(loader => {
                loader.style.display = 'none';
            });
        }
    }
    
    // Función asíncrona para crear gráficos de opción múltiple
    async function createChartAsync(questionId, options) {
        return new Promise((resolve, reject) => {
            try {
                const chartDom = document.getElementById(`chart-${questionId}`);
                if (!chartDom) {
                    return resolve(); // Resolving anyway to not block other charts
                }
                
                // Mostrar indicador de carga mientras se genera el gráfico
                const loadingEl = document.createElement('div');
                loadingEl.className = 'chart-loading';
                loadingEl.innerHTML = 'Generando gráfico...';
                loadingEl.style.textAlign = 'center';
                loadingEl.style.padding = '2rem';
                loadingEl.style.color = '#666';
                chartDom.appendChild(loadingEl);
                
                // Usar setTimeout para no bloquear el hilo principal
                setTimeout(() => {
                    try {
                        // Si ECharts ya no está disponible (e.g. usuario ha navegado a otra página)
                        if (typeof echarts === 'undefined') {
                            return resolve();
                        }
                        
                        const chart = echarts.init(chartDom);
                        
                        const names = options.map(opt => opt.name);
                        const values = options.map(opt => opt.value);
                        
                        // Determinar el tipo de gráfico en función del número de opciones
                        let chartType = 'pie';
                        let chartOption = {};
                        
                        if (options.length > 7) {
                            // Configuración para gráfico de barras
                            chartType = 'bar';
                            chartOption = {
                                tooltip: {
                                    trigger: 'axis',
                                    formatter: '{b}: {c}'
                                },
                                grid: {
                                    left: '3%',
                                    right: '4%',
                                    bottom: '3%',
                                    containLabel: true
                                },
                                xAxis: {
                                    type: 'value',
                                    name: 'Respuestas',
                                    nameLocation: 'middle',
                                    nameGap: 30
                                },
                                yAxis: {
                                    type: 'category',
                                    data: names,
                                    axisLabel: {
                                        interval: 0,
                                        rotate: 0
                                    }
                                },
                                series: [
                                    {
                                        name: 'Respuestas',
                                        type: 'bar',
                                        data: values,
                                        itemStyle: {
                                            color: function(params) {
                                                return chartColors[params.dataIndex % chartColors.length];
                                            }
                                        },
                                        label: {
                                            show: true,
                                            position: 'right',
                                            formatter: '{c}'
                                        }
                                    }
                                ]
                            };
                        } else {
                            // Para pocas opciones, usar gráfico circular
                            const totalVotes = values.reduce((acc, curr) => acc + curr, 0);
                            
                            // Formatear todas las opciones para la leyenda
                            const allFormattedOptions = options.map((opt, index) => {
                                const percentage = totalVotes > 0 ? ((opt.value / totalVotes) * 100).toFixed(1) : '0.0';
                                return {
                                    value: opt.value,
                                    name: opt.name,
                                    percentage: percentage + '%'
                                };
                            });
                            
                            // Solo incluir en el gráfico las opciones con valores > 0
                            const visibleOptions = allFormattedOptions.filter(opt => opt.value > 0);
                            
                            // Si no hay opciones con valores, mostrar un mensaje
                            if (visibleOptions.length === 0) {
                                loadingEl.remove();
                                chartDom.innerHTML = '<div class="no-data">No hay respuestas registradas para esta pregunta</div>';
                                return resolve();
                            }
                            
                            // Crear un objeto para buscar porcentajes rápidamente
                            const percentageMap = {};
                            allFormattedOptions.forEach(opt => {
                                percentageMap[opt.name] = opt.percentage;
                            });
                            
                            // Configuración para gráfico circular
                            chartOption = {
                                tooltip: {
                                    trigger: 'item',
                                    formatter: '{b}: {c} ({d}%)'
                                },
                                legend: {
                                    orient: 'vertical',
                                    right: 10,
                                    top: 'center',
                                    // Mostrar todas las opciones en la leyenda, incluso las de valor 0
                                    data: allFormattedOptions.map(opt => opt.name),
                                    formatter: function(name) {
                                        // Usar el mapa para recuperar el porcentaje por nombre
                                        return `${name}: ${percentageMap[name]}`;
                                    },
                                    textStyle: {
                                        // Opciones con 0% en gris claro
                                        color: function(name) {
                                            const opt = allFormattedOptions.find(o => o.name === name);
                                            return opt && opt.value === 0 ? '#999' : '#333';
                                        }
                                    }
                                },
                                series: [
                                    {
                                        name: 'Resultados',
                                        type: 'pie',
                                        radius: ['40%', '70%'],
                                        avoidLabelOverlap: false,
                                        // Solo mostrar en el gráfico las opciones con valores > 0
                                        data: visibleOptions,
                                        itemStyle: {
                                            color: function(params) {
                                                // Buscar el índice original para mantener los colores consistentes
                                                const originalIndex = allFormattedOptions.findIndex(
                                                    opt => opt.name === params.name
                                                );
                                                return chartColors[originalIndex % chartColors.length];
                                            },
                                            borderRadius: 10,
                                            borderColor: '#fff',
                                            borderWidth: 2
                                        },
                                        label: {
                                            show: true,
                                            position: 'inside',
                                            formatter: '{d}%',
                                            fontSize: 14,
                                            fontWeight: 'bold',
                                            color: '#fff'
                                        },
                                        emphasis: {
                                            label: {
                                                show: true,
                                                fontSize: 16,
                                                fontWeight: 'bold'
                                            },
                                            itemStyle: {
                                                shadowBlur: 10,
                                                shadowOffsetX: 0,
                                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                                            }
                                        }
                                    }
                                ]
                            };
                        }
                        
                        // Quitar el indicador de carga
                        loadingEl.remove();
                        
                        // Configurar el gráfico según el tipo
                        chart.setOption(chartOption);
                        
                        // Hacer el gráfico responsivo
                        const resizeListener = function() {
                            chart.resize();
                        };
                        
                        window.addEventListener('resize', resizeListener);
                        
                        // Cleanup function to remove event listener if chart is destroyed
                        chartDom.addEventListener('remove', function() {
                            window.removeEventListener('resize', resizeListener);
                        });
                        
                        resolve();
                    } catch (innerError) {
                        // Quitar el indicador de carga y mostrar un mensaje de error
                        if (loadingEl && loadingEl.parentNode) {
                            loadingEl.remove();
                        }
                        
                        chartDom.innerHTML = '<div class="chart-error">No se pudo generar el gráfico</div>';
                        resolve(); // Resolving anyway to not block other charts
                    }
                }, 0); // setTimeout with 0 pushes execution to the next event loop
                
            } catch (error) {
                resolve(); // Resolving anyway to not block other charts
            }
        });
    }
    
    // Función asíncrona para crear nubes de palabras
    async function createWordCloudAsync(questionId, answers) {
        return new Promise((resolve, reject) => {
            try {
                const wordcloudDom = document.getElementById(`wordcloud-${questionId}`);
                if (!wordcloudDom || !answers || !answers.length) {
                    return resolve();
                }
                
                // Mostrar indicador de carga mientras se genera la nube de palabras
                const loadingEl = document.createElement('div');
                loadingEl.className = 'chart-loading';
                loadingEl.innerHTML = 'Generando nube de palabras...';
                loadingEl.style.textAlign = 'center';
                loadingEl.style.padding = '2rem';
                loadingEl.style.color = '#666';
                wordcloudDom.appendChild(loadingEl);
                
                // Procesamiento de texto en segundo plano
                setTimeout(async () => {
                    try {
                        // Verificar si echarts sigue disponible
                        if (typeof echarts === 'undefined') {
                            return resolve();
                        }
                        
                        // Inicializar la instancia de ECharts
                        const wordcloud = echarts.init(wordcloudDom);
                        
                        // Procesar las respuestas para contar frecuencia de palabras (operación potencialmente costosa)
                        const wordFrequency = await processTextResponsesAsync(answers);
                        
                        if (wordFrequency.length === 0) {
                            loadingEl.remove();
                            wordcloudDom.innerHTML = '<div class="no-data">No hay suficientes datos para generar una nube de palabras</div>';
                            return resolve();
                        }
                        
                        // Configuración de la nube de palabras
                        const option = {
                            tooltip: {
                                show: true
                            },
                            series: [{
                                type: 'wordCloud',
                                shape: 'circle',
                                left: 'center',
                                top: 'center',
                                width: '90%',
                                height: '90%',
                                right: null,
                                bottom: null,
                                sizeRange: [12, 60],
                                rotationRange: [-45, 45],
                                rotationStep: 15,
                                gridSize: 8,
                                drawOutOfBound: false,
                                textStyle: {
                                    fontFamily: 'sans-serif',
                                    fontWeight: 'bold',
                                    color: function () {
                                        return 'rgb(' + [
                                            Math.round(Math.random() * 160 + 60),
                                            Math.round(Math.random() * 160 + 60),
                                            Math.round(Math.random() * 160 + 60)
                                        ].join(',') + ')';
                                    }
                                },
                                emphasis: {
                                    focus: 'self',
                                    textStyle: {
                                        shadowBlur: 10,
                                        shadowColor: '#333'
                                    }
                                },
                                data: wordFrequency
                            }]
                        };
                        
                        // Quitar el indicador de carga
                        loadingEl.remove();
                        
                        // Aplicar la configuración
                        wordcloud.setOption(option);
                        
                        // Hacer la nube de palabras responsiva
                        const resizeListener = function() {
                            wordcloud.resize();
                        };
                        
                        window.addEventListener('resize', resizeListener);
                        
                        // Cleanup function
                        wordcloudDom.addEventListener('remove', function() {
                            window.removeEventListener('resize', resizeListener);
                        });
                        
                        resolve();
                    } catch (innerError) {
                        // Quitar el indicador de carga y mostrar un mensaje de error
                        if (loadingEl && loadingEl.parentNode) {
                            loadingEl.remove();
                        }
                        
                        wordcloudDom.innerHTML = '<div class="chart-error">No se pudo generar la nube de palabras</div>';
                        resolve();
                    }
                }, 0);
                
            } catch (error) {
                resolve();
            }
        });
    }
    
    // Función asíncrona para procesar respuestas de texto
    async function processTextResponsesAsync(answers) {
        return new Promise(resolve => {
            setTimeout(() => {
                try {
                    // Lista extendida de stopwords en español
                    const stopWords = [
                        // Artículos
                        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'lo', 'al',
                        
                        // Pronombres
                        'yo', 'tu', 'él', 'ella', 'nosotros', 'nosotras', 'vosotros', 'vosotras', 
                        'ellos', 'ellas', 'me', 'te', 'se', 'nos', 'os', 'mi', 'mis', 'tu', 'tus', 
                        'su', 'sus', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 
                        'vuestros', 'vuestras', 'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 
                        'esas', 'aquel', 'aquella', 'aquellos', 'aquellas', 'le', 'les', 'lo', 'la', 
                        'los', 'las', 'quien', 'quienes', 'que', 'cual', 'cuales', 'cuanto', 'cuanta', 
                        'cuantos', 'cuantas', 'donde', 'cuando', 'como', 'yo', 'tú', 'él',
                        
                        // Preposiciones
                        'a', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 
                        'durante', 'en', 'entre', 'hacia', 'hasta', 'mediante', 'para', 
                        'por', 'según', 'sin', 'so', 'sobre', 'tras', 'versus', 'vía',
                        
                        // Conjunciones
                        'y', 'e', 'ni', 'o', 'u', 'bien', 'pero', 'aunque', 'sino', 'siquiera',
                        'mientras', 'porque', 'pues', 'ya', 'si', 'cuando', 'aunque', 'pues',
                        
                        // Verbos auxiliares y comunes (formas conjugadas)
                        'soy', 'eres', 'es', 'somos', 'sois', 'son', 'fui', 'fuiste', 'fue', 
                        'fuimos', 'fuisteis', 'fueron', 'ser', 'estar', 'estoy', 'estás', 'está', 
                        'estamos', 'estáis', 'están', 'he', 'has', 'ha', 'hemos', 'habéis', 
                        'han', 'había', 'habías', 'habíamos', 'habíais', 'habían', 'haber',
                        'tener', 'tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen',
                        'hacer', 'hago', 'haces', 'hace', 'hacemos', 'hacéis', 'hacen',
                        'poder', 'puedo', 'puedes', 'puede', 'podemos', 'podéis', 'pueden',
                        'decir', 'digo', 'dices', 'dice', 'decimos', 'decís', 'dicen',
                        'ir', 'voy', 'vas', 'va', 'vamos', 'vais', 'van',
                        'dar', 'doy', 'das', 'da', 'damos', 'dais', 'dan',
                        'ver', 'veo', 'ves', 've', 'vemos', 'veis', 'ven',
                        'saber', 'sé', 'sabes', 'sabe', 'sabemos', 'sabéis', 'saben',

                        // Adverbios comunes
                        'no', 'si', 'sí', 'más', 'menos', 'muy', 'mucho', 'muchos', 'mucha', 'muchas',
                        'poco', 'pocos', 'poca', 'pocas', 'algo', 'nada', 'demasiado', 'demasiada',
                        'bastante', 'bastantes', 'tan', 'tanto', 'tanta', 'tantos', 'tantas',
                        'aquí', 'allí', 'ahí', 'acá', 'allá', 'arriba', 'abajo', 'cerca', 'lejos',
                        'delante', 'detrás', 'encima', 'debajo', 'adentro', 'afuera',
                        'ahora', 'antes', 'después', 'luego', 'pronto', 'tarde', 'temprano',
                        'siempre', 'nunca', 'jamás', 'aún', 'todavía', 'ya',
                        'bien', 'mal', 'mejor', 'peor', 'regular', 'despacio', 'deprisa',
                        'así', 'también', 'solo', 'solamente', 'además', 'únicamente',
                        
                        // Palabras comunes en respuestas
                        'creo', 'pienso', 'opino', 'considero', 'parece', 'quiero', 'deseo',
                        'necesito', 'debería', 'podría', 'dice', 'cree', 'manera', 'forma',
                        'modo', 'tema', 'asunto', 'cosa', 'cosas', 'parte', 'partes',
                        'ejemplo', 'caso', 'casos', 'vez', 'veces',
                        'tipo', 'tipos', 'grupo', 'grupos', 'trabajo',
                        'días', 'día', 'semanas', 'semana', 'meses', 'mes', 'años', 'año',
                        'tiempo', 'momento', 'hora', 'horas', 'minutos',
                        'hay', 'sido', 'era', 'sea', 'ser', 'siendo',
                        'trata', 'existir', 'existe', 'existen', 'existiendo', 'existido',
                        
                        // Números escritos
                        'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez',
                        'primero', 'segundo', 'tercero', 'cuarto', 'quinto',
                        'primera', 'segunda', 'tercera', 'cuarta', 'quinta',
                        
                        // Demostrativos
                        'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas',
                        'aquel', 'aquella', 'aquellos', 'aquellas',
                        
                        // Tildes alternativas (para manejar errores comunes)
                        'qué', 'cómo', 'cuándo', 'dónde', 'quién', 'quiénes', 'cuál', 'cuáles',
                        'está', 'están', 'más', 'sí',
                        
                        // Palabras adicionales de baja relevancia semántica
                        'cada', 'todo', 'toda', 'todos', 'todas', 'alguno', 'alguna', 'algunos', 'algunas',
                        'ninguno', 'ninguna', 'ningunos', 'ningunas', 'otro', 'otra', 'otros', 'otras',
                        'mismo', 'misma', 'mismos', 'mismas', 'tan', 'tanto', 'tanta', 'tantos', 'tantas',
                        'tal', 'tales', 'demás', 'etc', 'etc.'
                    ];

                    // Set para búsquedas más eficientes
                    const stopWordsSet = new Set(stopWords);
                    
                    // Combinar todas las respuestas
                    const allText = answers.join(' ').toLowerCase();
                    
                    // Dividir en palabras y filtrar
                    const words = allText
                        // Eliminar puntuación y caracteres especiales
                        .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()¿?¡!"']/g, '')
                        // Reemplazar múltiples espacios con uno solo
                        .replace(/\s{2,}/g, ' ')
                        // Dividir por espacios
                        .split(' ')
                        // Filtrar palabras vacías y stopwords
                        .filter(word => {
                            return word && 
                                   word.length > 3 && 
                                   !stopWordsSet.has(word) && 
                                   isNaN(word); // Filtrar números
                        });
                    
                    // Contar frecuencia con Map para mejor rendimiento
                    const wordCountMap = new Map();
                    for (const word of words) {
                        wordCountMap.set(word, (wordCountMap.get(word) || 0) + 1);
                    }
                    
                    // Convertir a formato para ECharts y filtrar palabras poco frecuentes
                    const wordFrequency = Array.from(wordCountMap.entries())
                        .filter(([_, count]) => count > 1) // Solo palabras que aparecen más de una vez
                        .map(([word, count]) => ({
                            name: word,
                            value: count
                        }))
                        .sort((a, b) => b.value - a.value)
                        .slice(0, 100); // Limitar a 100 palabras máximo
                    
                    // Retornar el resultado procesado
                    resolve(wordFrequency);
                } catch (error) {
                    resolve([]);
                }
            }, 0);
        });
    }
    
    // Añadir estilos para los indicadores de carga y mensajes de error
    function addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .chart-loading {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 200px;
                color: #666;
                font-size: 0.9rem;
                background-color: rgba(255, 255, 255, 0.8);
            }
            
            .chart-loading::before {
                content: '';
                width: 20px;
                height: 20px;
                margin-right: 10px;
                border: 2px solid transparent;
                border-top-color: #1a73e8;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .chart-error {
                padding: 1rem;
                background-color: rgba(234, 67, 53, 0.1);
                border-left: 3px solid #ea4335;
                color: #ea4335;
                font-size: 0.9rem;
                text-align: center;
            }
            
            .no-data {
                padding: 2rem;
                color: #666;
                text-align: center;
                font-style: italic;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Iniciar el proceso
    addStyles();
    initCharts();
});