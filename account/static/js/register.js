document.addEventListener('DOMContentLoaded', function() {
    emailInput = document.getElementById('id_email');
    emailInput.addEventListener('input', function() {
        var emailValue = this.value;
        var username = emailValue.split('@')[0];
        var usernameInput = document.getElementById('username');
        usernameInput.value = username;
    });
});