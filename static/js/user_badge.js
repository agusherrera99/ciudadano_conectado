
document.addEventListener('DOMContentLoaded', function() {
    const dropdownMenu = document.querySelector('.dropdown-menu');
    document.querySelector('.user-badge').addEventListener('click', function(event) {
        event.preventDefault(); // Evitar que el enlace se siga inmediatamente.
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });

    const userBadge = document.querySelector('.user-badge');
    document.addEventListener('click', function(event) {
        if (!userBadge.contains(event.target)) {
            dropdownMenu.style.display = 'none';
        }
    });
});