document.addEventListener('DOMContentLoaded', function() {
    // Toggle section visibility
    const sectionToggles = document.querySelectorAll(".section-toggle");
    sectionToggles.forEach((toggle) => {
        toggle.addEventListener("click", function () {
            const sectionContent = this.nextElementSibling;
            const arrow = this.querySelector(".arrow");

            // Toggle the "open" class
            sectionContent.classList.toggle("open");

            // Rotate the arrow
            if (sectionContent.classList.contains("open")) {
                arrow.textContent = "▲";
            } else {
                arrow.textContent = "▼";
            }
        });
    });

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