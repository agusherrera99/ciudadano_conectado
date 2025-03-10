document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidad de filtrado por categoría
    const tabBtns = document.querySelectorAll('.tab-btn');
    const volunteeringCards = document.querySelectorAll('.volunteering-card');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Quitar clase activa de todos los botones
            tabBtns.forEach(b => b.classList.remove('active'));
            // Añadir clase activa al botón clickeado
            this.classList.add('active');
            
            const category = this.dataset.category;
            
            // Filtrar tarjetas según la categoría
            volunteeringCards.forEach(card => {
                if (category === 'all' || card.dataset.category === category) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Mostrar formulario de inscripción al presionar el botón de inscripción
    const opportunities = document.getElementById('opportunities');
    const myEnrollments = document.getElementById('my-enrollments');
    const applyForm = document.getElementById('apply-form');
    const closeFormBtn = document.getElementById('close-form-btn');
    
    // Variables para los campos del formulario
    const selectedTitle = document.getElementById('selected-volunteering-title');
    const selectedDescription = document.getElementById('selected-volunteering-description');
    const volunteeringIdField = document.getElementById('volunteering-id');

    // Cambiar de ID a clase para los botones de inscripción
    document.querySelectorAll('.volunteering-card').forEach(card => {
        // Solo procesar tarjetas donde el usuario no está inscrito
        if (!card.classList.contains('already-enrolled')) {
            const applyBtn = card.querySelector('#apply-btn');
            if (applyBtn) {
                // Asignar clase en lugar de id
                applyBtn.id = '';
                applyBtn.classList.add('apply-btn');
                
                // Obtener datos del voluntariado desde la tarjeta
                const title = card.querySelector('h3').textContent;
                const description = card.querySelector('.card-description').textContent;
                const volunteerId = card.getAttribute('data-id'); // Asegúrate de que las tarjetas tengan este atributo
                
                // Agregar listener al botón
                applyBtn.addEventListener('click', function() {
                    // Actualizar la información en el formulario
                    selectedTitle.textContent = title;
                    selectedDescription.textContent = description;
                    volunteeringIdField.value = volunteerId || '';
                    
                    // Mostrar el formulario y ocultar las oportunidades
                    opportunities.classList.add('hidden');
                    myEnrollments.classList.add('hidden');
                    applyForm.classList.remove('hidden');
                    
                    // Hacer scroll al formulario
                    applyForm.scrollIntoView({ behavior: 'smooth' });
                });
            }
        }
    });

    // Botón para cerrar el formulario
    if (closeFormBtn) {
        closeFormBtn.addEventListener('click', function() {
            applyForm.classList.add('hidden');
            opportunities.classList.remove('hidden');
            myEnrollments.classList.remove('hidden');
            
            // Volver a las oportunidades
            opportunities.scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Manejo de Envio de Formulario
    const volunteerForm = document.getElementById('volunteer-form');

    if (volunteerForm) {
        volunteerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validar el formulario
            const volunteerId = document.getElementById('volunteering-id').value;
            if (!volunteerId) {
                return;
            }
            
            // Preparar los datos del formulario
            const formData = new FormData(this);
            // Enviar el formulario
            fetch('/volunteering/apply/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});