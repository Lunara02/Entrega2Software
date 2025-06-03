async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem("token");
    const refreshToken = localStorage.getItem("refreshToken");
    
    if (!options.headers) {
        options.headers = {};
    }
    
    options.headers["Authorization"] = `Bearer ${token}`;
    
    let response = await fetch(url, options);
    
    if (response.status === 401) {
        try {
            const refreshResponse = await fetch("/api/token/refresh/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            });
            
            if (refreshResponse.ok) {
                const { access } = await refreshResponse.json();
                localStorage.setItem("token", access);
                options.headers["Authorization"] = `Bearer ${access}`;
                response = await fetch(url, options);
            } else {
                localStorage.removeItem("token");
                localStorage.removeItem("refreshToken");
                localStorage.removeItem("usuario");
                window.location.href = "/";
                throw new Error("Sesión expirada. Por favor inicia sesión nuevamente.");
            }
        } catch (error) {
            throw error;
        }
    }
    
    return response;
}

function verificarAutenticacion() {
    const token = localStorage.getItem("token");
    const usuario = JSON.parse(localStorage.getItem("usuario") || {});
    
    if (!token || usuario.tipo_usuario !== "admin") {
        window.location.href = "/";
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("usuario");
    window.location.href = "/";
}