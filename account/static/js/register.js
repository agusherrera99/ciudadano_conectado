document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navContent = document.getElementById('navContent');
    
    // Toggle sidebar
    navToggle.addEventListener('click', function() {
        navContent.classList.toggle('active');
    });

    // Close sidebar when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInside = navContent.contains(event.target) || navToggle.contains(event.target);
        
        if (!isClickInside && navContent.classList.contains('active')) {
            navContent.classList.remove('active');
        }
    });

    emailInput = document.getElementById('id_email');
    emailInput.addEventListener('input', function() {
        var emailValue = this.value;
        var username = emailValue.split('@')[0];
        var usernameInput = document.getElementById('username');
        usernameInput.value = username;
    });
});