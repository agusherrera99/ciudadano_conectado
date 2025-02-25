document.addEventListener('DOMContentLoaded', function() {
    // Manejo de votos
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            const issueId = this.dataset.id;
            const action = this.dataset.vote;
    
            const formData = new FormData();
            formData.append('action', action);
    
            fetch(`/issues/${issueId}/vote/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.querySelector('.votes-count').textContent = data.votes;
                } else {
                    console.error('Error al votar:', data.error);
                }
            })
            .catch(error => {
                console.error('There was an error:', error);
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

    // Enviar solicitud
    const requestForm = document.getElementById('request-form');
    requestForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        fetch('/issues/create/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();  // Recargar para ver la nueva solicitud
            } else {
                alert('Error al crear la solicitud');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al crear la solicitud');
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