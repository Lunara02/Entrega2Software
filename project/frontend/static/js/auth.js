// project/frontend/static/js/auth.js
// Funciones compartidas de autenticación

/**
 * Verifica si el usuario está autenticado
 * @returns {Promise<boolean>}
 */
export async function checkAuth() {
    try {
        const response = await fetch('/api/check-auth/', {
            credentials: 'include'
        });
        return response.ok;
    } catch (error) {
        console.error('Error verificando autenticación:', error);
        return false;
    }
}

/**
 * Obtiene información del usuario actual
 * @returns {Promise<Object|null>}
 */
export async function getCurrentUser() {
    try {
        const response = await fetch('/api/current-user/', {
            credentials: 'include'
        });
        
        if (response.ok) {
            return await response.json();
        }
        return null;
    } catch (error) {
        console.error('Error obteniendo usuario actual:', error);
        return null;
    }
}

/**
 * Redirige al login si no está autenticado
 */
export async function protectRoute() {
    const isAuthenticated = await checkAuth();
    if (!isAuthenticated) {
        window.location.href = '/login?next=' + encodeURIComponent(window.location.pathname);
    }
}

/**
 * Obtiene el valor de una cookie
 */
