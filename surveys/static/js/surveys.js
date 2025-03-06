document.addEventListener('DOMContentLoaded', function() {
    // Consultation participation
    const participateButtons = document.querySelectorAll('.participate');
    participateButtons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Redireccionar a página de participación en consulta');
        });
    });

    // Consultation results
    const viewResultsButtons = document.querySelectorAll('.view-survey-results');
    viewResultsButtons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Redireccionar a página de resultados de consulta');
        });
    });
});