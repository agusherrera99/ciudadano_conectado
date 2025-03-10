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
    const applyBtns = document.querySelectorAll('#apply-btn'); // Todos los botones tienen el mismo ID - problema
    const applyForm = document.getElementById('apply-form');
    const sectionIntro = document.getElementsByClassName('section-intro');
    const closeFormBtn = document.getElementById('close-form-btn');

    // Iterar sobre todos los botones de inscripción y agregar event listener a cada uno
    applyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            opportunities.classList.add('hidden');
            applyForm.classList.remove('hidden');
            
            // Hacer scroll al formulario
            applyForm.scrollIntoView({ behavior: 'smooth' });
        });
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