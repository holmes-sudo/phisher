// Password visibility toggle
const togglePassword = document.querySelector('#togglePassword');
const passwordField = document.querySelector('#passwordField');

if (togglePassword && passwordField) {
    togglePassword.addEventListener('click', function () {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        this.classList.toggle('fa-eye-slash');
    });
}

// Highlight empty fields on submit
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('sportyForm');
    const username = document.getElementById('usernameField');
    const password = document.getElementById('passwordField');
    const loginBtn = document.getElementById('loginBtn');

    function updateButtonColor() {
        if (username.value.trim() && password.value.trim()) {
            loginBtn.classList.add('active');
        } else {
            loginBtn.classList.remove('active');
        }
    }

    if (form && username && password && loginBtn) {
        username.addEventListener('input', updateButtonColor);
        password.addEventListener('input', updateButtonColor);
        updateButtonColor();

        form.addEventListener('submit', function (e) {
            let valid = true;
            if (!username.value.trim()) {
                username.classList.add('input-error');
                valid = false;
            } else {
                username.classList.remove('input-error');
            }
            if (!password.value.trim()) {
                password.classList.add('input-error');
                valid = false;
            } else {
                password.classList.remove('input-error');
            }
            if (!valid) e.preventDefault();
        });
    }
});