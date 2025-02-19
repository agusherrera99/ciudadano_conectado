document.addEventListener('DOMContentLoaded', function() {
    // Toggle new request form visibility
    const newRequestBtn = document.getElementById('new-request-btn');
    const newRequestForm = document.getElementById('new-request-form');
    const categorySelect = document.getElementById('category');
    const requestList = document.getElementById('request-list');
    const cancelRequestBtn = document.getElementById('cancel-request-btn');

    newRequestBtn.addEventListener('click', function() {
        newRequestBtn.classList.toggle('hidden');
        newRequestForm.classList.toggle('hidden');
        requestList.classList.toggle('hidden');
    });

    cancelRequestBtn.addEventListener('click', function() {
        newRequestBtn.classList.toggle('hidden');
        newRequestForm.classList.toggle('hidden');
        requestList.classList.toggle('hidden');
        // Reset form
        document.getElementById('request-form').reset();
    });

    // Form submission
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
        const selectedDate = filterDate.value;

        requestItems.forEach(item => {
            const type = item.querySelector('.request-type').textContent.toLowerCase();
            const status = item.querySelector('.request-status').textContent.toLowerCase();
            const date = item.querySelector('.request-date').textContent.split(': ')[1].split('T')[0];

            const matchesType = !selectedType || type === selectedType;
            const matchesStatus = !selectedStatus || status === selectedStatus;
            const matchesDate = !selectedDate || date === selectedDate;

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