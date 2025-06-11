// project/frontend/static/js/logout.js
import { getCookie } from './utils.js';
document.addEventListener('DOMContentLoaded', function() {
    const logoutButtons = document.querySelectorAll('.logout-btn');
    
    logoutButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            
            try {
                const response = await fetch('/api/logout/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    credentials: 'include'
                });

                if (response.ok) {
                    window.location.href = '/login';
                } else {
                    const data = await response.json();
                    throw new Error(data.error || 'Error al cerrar sesión');
                }
            } catch (error) {
                console.error('Error en logout:', error);
                alert(error.message);
            }
        });
    });
});

