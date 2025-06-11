// project/frontend/static/js/login.js
import { getCookie } from './utils.js';
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const mensajeError = document.getElementById('mensaje-error');
    const loadingIndicator = document.getElementById('loading-indicator');

    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            loadingIndicator.classList.remove('d-none');
            mensajeError.textContent = '';
            mensajeError.classList.add('d-none');

            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('/api/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    credentials: 'include',
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || 'Error en el inicio de sesión');
                }

                // Redirección basada en rol
                redirectByRole(data.user.rol);

            } catch (error) {
                console.error('Error en login:', error);
                mensajeError.textContent = error.message;
                mensajeError.classList.remove('d-none');
            } finally {
                loadingIndicator.classList.add('d-none');
            }
        });
    }
});

function redirectByRole(rol) {
    const rolesRedirect = {
        'cliente': '/panel/usuario',
        'conductor': '/panel/conductor',
        'admin': '/panel/admin'
    };

    const redirectPath = rolesRedirect[rol];
    if (redirectPath) {
        window.location.href = redirectPath;
    } else {
        throw new Error(`Rol no reconocido: ${rol}`);
    }
}
