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
});