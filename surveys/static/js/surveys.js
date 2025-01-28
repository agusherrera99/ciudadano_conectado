document.addEventListener('DOMContentLoaded', function() {
    // Consultation participation
    const participateButtons = document.querySelectorAll('.participate');
    participateButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Here you would typically open a participation form or modal
            alert('Redireccionar a página de participación en consulta');
        });
    });

    // Consultation results
    const viewResultsButtons = document.querySelectorAll('.view-survey-results');
    viewResultsButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Here you would typically fetch and display the results
            alert('Redireccionar a página de resultados de consulta');
        });
    });
});