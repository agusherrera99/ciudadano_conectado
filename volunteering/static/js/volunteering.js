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
    const applyForm = document.getElementById('apply-form');
    const closeFormBtn = document.getElementById('close-form-btn');
    
    // Variables para los campos del formulario
    const selectedTitle = document.getElementById('selected-volunteering-title');
    const selectedDescription = document.getElementById('selected-volunteering-description');
    const volunteeringIdField = document.getElementById('volunteering-id');

    // Cambiar de ID a clase para los botones de inscripción
    document.querySelectorAll('.volunteering-card').forEach(card => {
        // Cambiar el selector de ID a selector de clase
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
                applyForm.classList.remove('hidden');
                
                // Hacer scroll al formulario
                applyForm.scrollIntoView({ behavior: 'smooth' });
            });
        }
    });

    // Botón para cerrar el formulario
    if (closeFormBtn) {
        closeFormBtn.addEventListener('click', function() {
            applyForm.classList.add('hidden');
            opportunities.classList.remove('hidden');
            
            // Volver a las oportunidades
            opportunities.scrollIntoView({ behavior: 'smooth' });
        });
    }
});