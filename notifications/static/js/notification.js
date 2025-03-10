document.addEventListener('DOMContentLoaded', function() {
    // Función para marcar notificaciones como leídas
    const markReadButtons = document.querySelectorAll('.mark-read-btn');
    
    markReadButtons.forEach(button => {
        button.addEventListener('click', function() {
            const notificationItem = this.closest('.notification-item');
            const notificationId = notificationItem.dataset.id;
            
            // Añadir efecto visual inmediato
            notificationItem.classList.remove('unread');
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-check-double"></i>';
            
            // Animación de desvanecimiento para el botón
            setTimeout(() => {
                button.style.opacity = '0';
                
                setTimeout(() => {
                    button.remove();
                }, 300);
            }, 500);
            
            // Cambiar el icono de la notificación
            const icon = notificationItem.querySelector('i:first-child');
            if (icon && icon.classList.contains('fa-circle-exclamation')) {
                icon.classList.remove('fa-circle-exclamation');
                icon.classList.add('fa-bell');
            }
            
            // Enviar solicitud al servidor para marcar como leída
            fetch(`/notifications/mark-read/${notificationId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ read: true })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('No se pudo marcar la notificación como leída');
                }
                return response.json();
            })
            .then(data => {
                location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
                // Revertir cambios visuales en caso de error
                notificationItem.classList.add('unread');
                button.disabled = false;
                button.innerHTML = '<i class="fas fa-check"></i>';
                button.style.opacity = '1';
            });
        });
    });
    
    // Función para obtener el valor de una cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Optimizaciones para dispositivos móviles
    function checkMobileLayout() {
        const isMobile = window.innerWidth <= 480;
        const notificationItems = document.querySelectorAll('.notification-item');
        
        notificationItems.forEach(item => {
            // En móviles, asegurar que los elementos estén bien organizados
            if (isMobile) {
                item.classList.add('mobile-view');
            } else {
                item.classList.remove('mobile-view');
            }
        });
    }
    
    // Comprobar el layout al cargar y al cambiar el tamaño de la ventana
    checkMobileLayout();
    window.addEventListener('resize', checkMobileLayout);
});