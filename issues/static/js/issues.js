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
});