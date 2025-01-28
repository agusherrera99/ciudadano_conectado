document.addEventListener('DOMContentLoaded', function() {
    // Toggle new request form visibility
    const newRequestBtn = document.getElementById('new-request-btn');
    const newRequestForm = document.getElementById('new-request-form');
    const requestTypeSelect = document.getElementById('request-type');
    const requestList = document.getElementById('request-list')
    const cancelRequestBtn = document.getElementById('cancel-request-btn');

    newRequestBtn.addEventListener('click', function() {
        newRequestBtn.classList.toggle('hidden');
        newRequestForm.classList.toggle('hidden');
        requestList.classList.toggle('hidden')
    });

    cancelRequestBtn.addEventListener('click', function() {
        newRequestBtn.classList.toggle('hidden');
        newRequestForm.classList.toggle('hidden');
        requestList.classList.toggle('hidden')
    });

    // Toggle request type form visibility
    requestTypeSelect.addEventListener('change', function() {
        const selectedType = requestTypeSelect.value;
        
        const publicObjectsContainer = document.getElementById('public-objects-container');
        const complaintContainer = document.getElementById('complaint-container');
        const suggestionContainer = document.getElementById('suggestion-container');

        if (selectedType === 'maintenance') {
            publicObjectsContainer.classList.remove('hidden');
            complaintContainer.classList.add('hidden');
            suggestionContainer.classList.add('hidden');

            const publicObjectsCategory = document.getElementById('public-objects-category');

            publicObjectsCategory.addEventListener('change', function() {
                const selectedCategory = publicObjectsCategory.value;
                const publicObjects = document.getElementById('public-objects');

                if (selectedCategory === 'lights') {
                    publicObjects.classList.remove('hidden');
                    renderObjects();
                } else {
                    publicObjects.classList.add('hidden');
                }
            });
        } else if (selectedType === 'complaint') {
            complaintContainer.classList.remove('hidden');
            publicObjectsContainer.classList.add('hidden');
            suggestionContainer.classList.add('hidden');
        } else if (selectedType === 'suggestion') {
            suggestionContainer.classList.remove('hidden');
            publicObjectsContainer.classList.add('hidden');
            complaintContainer.classList.add('hidden');
        }   
    });

    // Request details
    const viewDetailsButtons = document.querySelectorAll('.request-details');
    viewDetailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Here you would typically fetch the details and display them
            alert('Redireccionar a página de detalles de solicitud');
        });
    });
});