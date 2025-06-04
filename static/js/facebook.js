document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');

    if (togglePassword && password) {
        togglePassword.addEventListener('click', function () {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            this.textContent = type === 'password' ? 'Show' : 'Hide';
        });
    }
});

// User validation function using getElementById
function login(event) {
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    let valid = true;

    username.style.border = '';
    password.style.border = '';

    if (!username.value.trim()) {
        username.style.border = '2px solid red';
        valid = false;
    }
    if (!password.value.trim()) {
        password.style.border = '2px solid red';
        valid = false;
    }

    if (!valid) {
        event.preventDefault();
        return false;
    }
    return true;
}

