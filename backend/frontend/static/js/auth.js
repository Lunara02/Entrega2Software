// project/static/js/auth.js

// URL base de tu API (ajusta si no es localhost:8000)
const API_BASE = window.location.origin + '/api';

// Campo donde mostrar errores
const errorDiv = document.getElementById('error');

// Función para enviar el formulario de login
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorDiv.textContent = '';

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_BASE}/users/token/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                const errData = await response.json();
                errorDiv.textContent = errData.detail || 'Credenciales inválidas.';
                return;
            }

            const data = await response.json();
            // Almacena access y refresh en localStorage
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);

            // Redirige a /panel/
            window.location.href = '/panel/';
        } catch (err) {
            console.error(err);
            errorDiv.textContent = 'Error de conexión.';
        }
    });
});

// Función para cerrar sesión (borrar tokens y redirigir)
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/';
}

// Si estamos en 'panel.html', asignamos el botón de logout:
document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
});
