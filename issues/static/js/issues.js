document.addEventListener('DOMContentLoaded', function() {
    // Manejo de votos
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            const issueId = this.dataset.id;
            const action = this.dataset.vote;
    
            const formData = new FormData();
            formData.append('action', action);
    
            fetch(`/solicitudes/${issueId}/votar/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status) {
                    document.querySelector('.votes-count').textContent = data.votes;
                    location.reload();
                } else {
                    console.error('Error al votar:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
    

    // Botón y formulario de nueva solicitud
    const newRequestBtn = document.getElementById('new-request-btn');
    const newRequestForm = document.getElementById('new-request-form');
    const categorySelect = document.getElementById('category');
    const userRequests = document.getElementById('user-requests');
    const cancelRequestBtn = document.getElementById('cancel-request-btn');

    newRequestBtn.addEventListener('click', function() {
        newRequestBtn.classList.toggle('hidden');
        newRequestForm.classList.toggle('hidden');
        userRequests.classList.toggle('hidden');
    });

    cancelRequestBtn.addEventListener('click', function() {
        newRequestBtn.classList.toggle('hidden');
        newRequestForm.classList.toggle('hidden');
        userRequests.classList.toggle('hidden');

        document.getElementById('request-form').reset();
    });

    // Mapa para ubicación de reclamos
    let map = null;
    let marker = null;
    const locationContainer = document.getElementById('location-container');
    
    // Mostrar u ocultar el mapa según la categoría seleccionada
    categorySelect.addEventListener('change', function() {
        if (this.value === 'reclamo') {
            locationContainer.classList.remove('hidden');
            setTimeout(initMap, 100); // Pequeño retraso para asegurar que el contenedor es visible
        } else {
            locationContainer.classList.add('hidden');
        }
    });

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

    // Enviar solicitud
    const requestForm = document.getElementById('request-form');
    requestForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validar que se haya seleccionado ubicación para reclamos
        const category = categorySelect.value;
        const latitude = document.getElementById('latitude').value;
        const longitude = document.getElementById('longitude').value;
        
        if (category === 'reclamo' && (!latitude || !longitude)) {
            alert('Por favor, indica la ubicación del reclamo en el mapa.');
            return;
        }
        
        const formData = new FormData(this);
        fetch('/solicitudes/crear/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                requestForm.reset();
                location.reload();
            } else {
                alert('Error al enviar la solicitud');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión al enviar la solicitud');
        });
    });

    // Filtrado de solicitudes
    const filterType = document.getElementById('filter-type');
    const filterStatus = document.getElementById('filter-status');
    const filterDate = document.getElementById('filter-date');
    const requestItems = document.querySelectorAll('.request-item');

    function filterRequests() {
        const selectedType = filterType.value.toLowerCase();
        const selectedStatus = filterStatus.value.toLowerCase();
        const selectedDate = filterDate.value; // Formato: YYYY-MM-DD

        requestItems.forEach(item => {
            const type = item.querySelector('.request-type').textContent.toLowerCase();
            const status = item.querySelector('.request-status').textContent.toLowerCase();
            
            // Convertir la fecha del item (DD-MM-YYYY) a YYYY-MM-DD para comparar
            const dateStr = item.querySelector('.user-request-date').textContent.trim();
            const [day, month, year] = dateStr.split('-');
            const formattedDate = `${year}-${month}-${day}`;

            const matchesType = !selectedType || type === selectedType;
            const matchesStatus = !selectedStatus || status === selectedStatus;
            const matchesDate = !selectedDate || formattedDate === selectedDate;

            if (matchesType && matchesStatus && matchesDate) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    }

    // Agregar event listeners para los filtros
    filterType.addEventListener('change', filterRequests);
    filterStatus.addEventListener('change', filterRequests);
    filterDate.addEventListener('input', filterRequests);

    // Agregar botón para limpiar filtros
    const filtersDiv = document.querySelector('.filters');
    const clearFiltersBtn = document.getElementById('clearFilterBtn');
    
    clearFiltersBtn.addEventListener('click', () => {
        filterType.value = '';
        filterStatus.value = '';
        filterDate.value = '';
        requestItems.forEach(item => item.style.display = '');
    });
    filtersDiv.appendChild(clearFiltersBtn);
});