document.addEventListener('DOMContentLoaded', function() {
    const newRequestBtn = document.getElementById('new-request-btn');
    const newRequestForm = document.getElementById('new-request-form');
    const requestList = document.getElementById('request-list')

    newRequestBtn.addEventListener('click', function() {
        newRequestForm.classList.toggle('hidden');
        requestList.classList.toggle('hidden')
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