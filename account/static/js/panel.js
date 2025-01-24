document.addEventListener('DOMContentLoaded', function() {
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

    const objectCards = document.getElementById("object-cards");
    const searchInput = document.getElementById("search");
    const searchButton = document.getElementById("search-button");

    // Example data (replace with real data from a backend)
    const objects = [
        { id: 1, identifier: "Light #1234", location: "Calle Principal", latitude: -34.6037, longitude: -58.3816 },
        { id: 2, identifier: "Light #5678", location: "Avenida Libertador", latitude: -34.5915, longitude: -58.3814 },
        { id: 3, identifier: "Light #9101", location: "Plaza de Mayo", latitude: -34.6083, longitude: -58.3712 },
        { id: 4, identifier: "Light #1121", location: "Parque Centenario", latitude: -34.6055, longitude: -58.4352 },
    ];

    // Render object cards
    function renderObjects(searchQuery = "") {
        objectCards.innerHTML = "";
        const filteredObjects = objects.filter((obj) =>
            obj.identifier.toLowerCase().includes(searchQuery.toLowerCase())
        );

        filteredObjects.forEach((obj) => {
            const card = document.createElement("div");
            card.className = "card";
            card.innerHTML = `
                <h3>${obj.identifier}</h3>
                <p>${obj.location}</p>
            `;
            objectCards.appendChild(card);
        });
    }

    // Handle search
    searchButton.addEventListener("click", () => {
        renderObjects(searchInput.value);
    });


    const viewDetailsButtons = document.querySelectorAll('.view-details');
    viewDetailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Here you would typically fetch the details and display them
            alert('Request details would be shown here.');
        });
    });

    const participateButtons = document.querySelectorAll('.participate');
    participateButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Here you would typically open a participation form or modal
            alert('Participation form would be shown here.');
        });
    });

    const viewResultsButtons = document.querySelectorAll('.view-results');
    viewResultsButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Here you would typically fetch and display the results
            alert('Consultation results would be shown here.');
        });
    });
});