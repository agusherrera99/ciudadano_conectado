document.addEventListener('DOMContentLoaded', function() {
    const editProfileBtn = document.getElementById('edit-profile-btn');
    const editProfileForm = document.getElementById('edit-profile-form');
    const cancelEditProfileBtn = document.getElementById('cancel-edit-profile-btn');
    const profileDetails = document.querySelector('.profile-details');

    // Toggle edit profile form
    editProfileBtn.addEventListener('click', function() {
        editProfileForm.classList.remove('hidden');
        profileDetails.classList.add('hidden');
        editProfileBtn.classList.add('hidden');
    });

    cancelEditProfileBtn.addEventListener('click', function(e) {
        e.preventDefault();
        editProfileForm.classList.add('hidden');
        profileDetails.classList.remove('hidden');
        editProfileBtn.classList.remove('hidden');
    });

    // Handle form submission
    const form = editProfileForm.querySelector('form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        fetch(window.location.pathname, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});