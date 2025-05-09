document.addEventListener('DOMContentLoaded', function() {
    // Mapa para ubicación de reclamos
    let map = null;
    let marker = null;

    // Inicializar mapa
    function initMap() {
        if (map !== null) return; // Evitar inicializar múltiples veces
        
        const defaultLat = -36.01398;
        const defaultLng = -59.09992;

        map = L.map('location-map').setView([defaultLat, defaultLng], 13);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Intentar obtener la ubicación actual del usuario
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    map.setView([lat, lng], 15);
                },
                function(error) {
                    throw new Error('Error al obtener ubicación:', error);
                }
            );
        }

        // Manejar clics en el mapa
        map.on('click', function(e) {
            const lat = e.latlng.lat;
            const lng = e.latlng.lng;
            
            // Actualizar campos ocultos
            document.getElementById('latitude').value = lat;
            document.getElementById('longitude').value = lng;
            
            // Actualizar marcador
            if (marker) {
                marker.setLatLng([lat, lng]);
            } else {
                marker = L.marker([lat, lng]).addTo(map);
            }
            
            // Obtener dirección mediante geocodificación inversa
            fetchAddress(lat, lng);
        });
    }

    // Geocodificación inversa usando Nominatim
    function fetchAddress(lat, lng) {
        fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`)
            .then(response => response.json())
            .then(data => {
                const address = data.display_name || 'Dirección desconocida';
                document.getElementById('address').value = address;
            })
            .catch(error => {
                console.error('Error al obtener dirección:', error);
                document.getElementById('address').value = 'No se pudo determinar la dirección';
            });
    }
    initMap();

    // Formulario de nuevo ordenamiento
    const orderForm = document.getElementById('order-form');
    
    // Enviar Nuevo Ordenamiento
    orderForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Validar que se haya seleccionado ubicación para reclamos
        const latitude = document.getElementById('latitude').value;
        const longitude = document.getElementById('longitude').value;

        if ((!latitude || !longitude)) {
            alert('Por favor, indica la ubicación del reclamo en el mapa.');
            return;
        }
        
        const formData = new FormData(orderForm);

        // Cambio de texto del botón de envío
        const submitButton = orderForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.innerHTML;
        submitButton.disabled = true;
        submitButton.innerHTML = 'Enviando...';
        
        fetch('/ordenamientos-urbanos/crear/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            // Verificar el estado de la respuesta primero
            if (!response.ok) {
                console.error(`Error HTTP: ${response.status} ${response.statusText}`);
                return response.text().then(text => {
                    throw new Error(`Error del servidor: ${response.status} ${response.statusText}\nContenido: ${text.substring(0, 200)}...`);
                });
            }
            
            // Comprobar el tipo de contenido para saber si es JSON
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json();
            } else {
                return response.text().then(text => {
                    console.error('La respuesta no es JSON:', text.substring(0, 200));
                    throw new Error('La respuesta del servidor no es JSON válido');
                });
            }
        })
        .then(data => {
            console.log('Datos recibidos del servidor:', data);

            // Restaurar el estado del botón
            submitButton.disabled = false;
            submitButton.innerHTML = originalButtonText;
            
            if (data.status) {
                console.log('Ordenamiento creado exitosamente');
                orderForm.reset();
                location.reload();
                alert('Ordenamiento creado exitosamente');
            } else {
                console.error('Error al enviar ordenamiento:', data.error || 'Error desconocido');
                console.error('Datos completos de error:', data);
                alert('Error al enviar la solicitud: ' + (data.error || 'Error desconocido'));
            }
        })
        .catch(error => {
            console.error('Error completo:', error);
            console.error('Stack trace:', error.stack);
            console.error('Mensaje:', error.message);
            
            // Restaurar el estado del botón también en caso de error
            submitButton.disabled = false;
            submitButton.innerHTML = originalButtonText;
            
            // Mostrar un mensaje más informativo
            alert('Error al procesar la solicitud: ' + error.message);
        });
    });
    
    // Cancelar nuevo ordenamiento
    const cancelOrderBtn = document.getElementById('cancel-order-btn');

    cancelOrderBtn.addEventListener('click', function() {
        if (marker) {
            map.removeLayer(marker);
            marker = null;
        }

        orderForm.reset();
    });

});