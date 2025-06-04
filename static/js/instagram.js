document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.getElementById('togglePassword');
    const passwordField = document.getElementById('passwordField');
    const loginForm = document.getElementById('loginForm');
    const usernameField = document.getElementById('usernameField');
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');

    // Toggle password visibility
    togglePassword.addEventListener('click', function () {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        this.querySelector('i').classList.toggle('fa-eye');
        this.querySelector('i').classList.toggle('fa-eye-slash');
    });

    // Form validation
    loginForm.addEventListener('submit', function (e) {
        let isValid = true;

        // Reset errors
        usernameField.classList.remove('error');
        passwordField.classList.remove('error');
        usernameError.style.display = 'none';
        passwordError.style.display = 'none';

        // Validate username
        if (!usernameField.value.trim()) {
            usernameField.classList.add('error');
            usernameError.style.display = 'block';
            isValid = false;
        }

        // Validate password
        if (!passwordField.value.trim()) {
            passwordField.classList.add('error');
            passwordError.style.display = 'block';
            isValid = false;
        }

        // Only prevent submission if invalid
        if (!isValid) {
            e.preventDefault();
        }
        // If valid, allow form to submit to Flask backend
    });

    // Clear error when user starts typing
    usernameField.addEventListener('input', function () {
        if (this.classList.contains('error')) {
            this.classList.remove('error');
            usernameError.style.display = 'none';
        }
    });

    passwordField.addEventListener('input', function () {
        if (this.classList.contains('error')) {
            this.classList.remove('error');
            passwordError.style.display = 'none';
        }
    });
});