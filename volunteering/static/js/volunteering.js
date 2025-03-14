document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidad de filtrado por categoría
    const tabBtns = document.querySelectorAll('.tab-btn');
    const volunteeringCards = document.querySelectorAll('.volunteering-card');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            tabBtns.forEach(b => b.classList.remove('active'));
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
    
    // manejo de formulario de inscripción
    const applyBtns = document.querySelectorAll('#apply-btn');
    
    applyBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const card = this.closest('.volunteering-card');
            const title = card.querySelector('h3').textContent;
            const description = card.querySelector('.card-description').textContent;
            const volunteerId = card.getAttribute('data-id');
            
            // Ocultar secciones
            const opportunities = document.getElementById('opportunities');
            const myEnrollments = document.getElementById('my-enrollments');
            const applyForm = document.getElementById('apply-form');
            
            if (opportunities) opportunities.classList.add('hidden');
            if (myEnrollments) myEnrollments.classList.add('hidden');
            
            // Actualizar y mostrar formulario
            if (applyForm) {
                const selectedTitle = document.getElementById('selected-volunteering-title');
                const selectedDescription = document.getElementById('selected-volunteering-description');
                const volunteeringIdField = document.getElementById('volunteering-id');
                
                if (selectedTitle) selectedTitle.textContent = title;
                if (selectedDescription) selectedDescription.textContent = description;
                if (volunteeringIdField) volunteeringIdField.value = volunteerId || '';
                
                applyForm.classList.remove('hidden');
                applyForm.scrollIntoView({ behavior: 'smooth' });
            } else {
                console.error("Elemento #apply-form no encontrado");
            }
        });
    });
    
    // botón de cerrar formulario
    const closeFormBtn = document.getElementById('close-form-btn');
    if (closeFormBtn) {
        closeFormBtn.addEventListener('click', function() {
            
            const opportunities = document.getElementById('opportunities');
            const myEnrollments = document.getElementById('my-enrollments');
            const applyForm = document.getElementById('apply-form');
            
            if (applyForm) applyForm.classList.add('hidden');
            if (opportunities) opportunities.classList.remove('hidden');
            if (myEnrollments) myEnrollments.classList.remove('hidden');
            
            if (opportunities) opportunities.scrollIntoView({ behavior: 'smooth' });
        });
    } else {
        console.error("Elemento #close-form-btn no encontrado");
    }

    // manejo de checkboxes de disponibilidad
    var checkboxes = document.querySelectorAll('.availability-checkbox');
    
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            // Si cualquier checkbox está marcado, quitar el required de todos
            var anyChecked = Array.from(checkboxes).some(cb => cb.checked);
            
            checkboxes.forEach(function(cb) {
                cb.required = !anyChecked;
            });
        });
    });
    
    // enviar formulario
    const volunteerForm = document.getElementById('volunteer-form');
    if (volunteerForm) {
        volunteerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const volunteerId = document.getElementById('volunteering-id')?.value;
            if (!volunteerId) {
                console.error("No se ha seleccionado un voluntariado");
                return;
            }
            
            // Preparar los datos del formulario
            const formData = new FormData(this);
            
            // Enviar el formulario
            fetch('/voluntariados/aplicar/', {
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
                if (data.status) {
                    location.reload();
                } else {
                    console.error("Error en respuesta:", data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    } else {
        console.error("Elemento #volunteer-form no encontrado");
    }
});