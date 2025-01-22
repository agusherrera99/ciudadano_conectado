document.addEventListener('DOMContentLoaded', function() {
    const editProfileBtn = document.getElementById('edit-profile-btn');
    const editProfileForm = document.getElementById('edit-profile-form');
    const cancelEditProfileBtn = document.getElementById('cancel-edit-profile-btn');
    const saveEditProfileBtn = document.getElementById('save-edit-profile-btn');

    editProfileBtn.addEventListener('click', function() {
        editProfileBtn.classList.toggle('hidden');
        editProfileForm.classList.toggle('hidden');
    });

    cancelEditProfileBtn.addEventListener('click', function() {
        editProfileBtn.classList.toggle('hidden');
        editProfileForm.classList.toggle('hidden');
    });

    saveEditProfileBtn.addEventListener('click', function() {
        alert('Request details would be shown here.');
    });

    const changePasswordBtn = document.getElementById('change-password-btn');
    const changePasswordForm = document.getElementById('change-password-form');
    const cancelChangePasswordBtn = document.getElementById('cancel-change-password-btn');
    const saveChangePasswordBtn = document.getElementById('save-change-password-btn');

    changePasswordBtn.addEventListener('click', function() {
        changePasswordBtn.classList.toggle('hidden');
        changePasswordForm.classList.toggle('hidden');
    });

    cancelChangePasswordBtn.addEventListener('click', function() {
        changePasswordBtn.classList.toggle('hidden');
        changePasswordForm.classList.toggle('hidden');
    });

    saveChangePasswordBtn.addEventListener('click', function() {
        alert('Request details would be shown here.');
    });
});