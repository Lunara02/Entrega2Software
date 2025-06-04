// project/static/js/auth.js

// URL base de tu API (ajusta si no es localhost:8000)
const API_BASE = window.location.origin + '/api';

// Campo donde mostrar errores
const errorDiv = document.getElementById('error');

// Función para enviar el formulario de login
document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = window.location.origin + '/api';

    const btnLogin = document.getElementById("btnLogin");
    const btnRegistro = document.getElementById("btnRegistro");
    const btnEntrar = document.getElementById("btnEntrar");
    const btnCrearUsuario = document.getElementById("btnCrearUsuario");

    const loginForm = document.getElementById("loginForm");
    const registroForm = document.getElementById("registroForm");
    const respuesta = document.getElementById("respuesta");

    // Mostrar formulario de login
    btnLogin.addEventListener("click", () => {
        loginForm.classList.remove("d-none");
        registroForm.classList.add("d-none");
        respuesta.textContent = '';
    });

    // Mostrar formulario de registro
    btnRegistro.addEventListener("click", () => {
        registroForm.classList.remove("d-none");
        loginForm.classList.add("d-none");
        respuesta.textContent = '';
    });

    // Iniciar sesión
    btnEntrar.addEventListener("click", async () => {
        const correo = document.getElementById("correo").value.trim();
        const contrasena = document.getElementById("contrasena").value;

        respuesta.textContent = "Cargando...";

        try {
            const res = await fetch(`${API_BASE}/token/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: correo, password: contrasena })
            });

            const data = await res.json();

            if (!res.ok) {
                respuesta.textContent = data.detail || "Credenciales inválidas.";
                return;
            }

            localStorage.setItem("access_token", data.access);
            localStorage.setItem("refresh_token", data.refresh);
            respuesta.textContent = "¡Login exitoso! Redirigiendo...";
            window.location.href = "/panel/";
        } catch (err) {
            console.error(err);
            respuesta.textContent = "Error de conexión al iniciar sesión.";
        }
    });

    // Registrar usuario
    btnCrearUsuario.addEventListener("click", async () => {
        const nombre = document.getElementById("nombreNuevo").value.trim();
        const correo = document.getElementById("correoNuevo").value.trim();
        const clave = document.getElementById("claveNuevo").value;
        const rol = document.getElementById("rolNuevo").value;

        respuesta.textContent = "Registrando...";

        try {
            const res = await fetch(`${API_BASE}/usuarios/crear/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ nombre, correo, clave, rol })
            });

            const data = await res.json();

            if (!res.ok) {
                respuesta.textContent = data.detail || "Error al registrar.";
                return;
            }

            respuesta.textContent = "Usuario creado correctamente. Ya puedes iniciar sesión.";
        } catch (err) {
            console.error(err);
            respuesta.textContent = "Error de conexión al registrar.";
        }
    });

    // Cerrar sesión (por si lo necesitas en /panel/)
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/';
        });
    }
});

