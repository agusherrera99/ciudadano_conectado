document.addEventListener('DOMContentLoaded', function() {
    const surveyForm = document.getElementById('survey-form');

    if (surveyForm) {
        surveyForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Mostrar indicador de carga
            const submitButton = surveyForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.textContent = 'Enviando...';
            submitButton.disabled = true;
            
            // Obtener todos los datos del formulario
            const formData = new FormData(surveyForm);
            const surveyId = surveyForm.getAttribute('data-survey-id');
            
            // Enviar los datos al servidor
            await fetch(`/surveys/${surveyId}/submit/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                // Si fue exitoso, redirigir después de un tiempo
                if (data.status) {
                    location.reload();
                } else {
                    // Restaurar el botón si hay error
                    submitButton.textContent = originalButtonText;
                    submitButton.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Restaurar el botón si hay error
                submitButton.textContent = originalButtonText;
                submitButton.disabled = false
            });
        });
    }
});