document.addEventListener('DOMContentLoaded', function() {
    const dropdownMenu = document.querySelector('.dropdown-menu');
    document.querySelector('.user-badge').addEventListener('click', function(event) {
        event.preventDefault(); // Evitar que el enlace se siga inmediatamente.
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });

    const userBadgeContainer = document.querySelector('.user-badge-container');
    document.addEventListener('click', function(event) {
        if (!userBadgeContainer.contains(event.target)) {
            dropdownMenu.style.display = 'none';
        }
    });
});