// project/static/js/app.js

// URL base para la API
const API_BASE = window.location.origin + '/api';

// Obtener el token de acceso del localStorage
function getAccessToken() {
    return localStorage.getItem('access_token');
}

// Función genérica para hacer peticiones con JWT en la cabecera
async function fetchWithAuth(url, options = {}) {
    const token = getAccessToken();
    if (!token) {
        // Si no hay token, redirige al login
        window.location.href = '/';
        return;
    }

    const headers = options.headers || {};
    headers['Authorization'] = `Bearer ${token}`;
    headers['Content-Type'] = 'application/json';
    options.headers = headers;

    const response = await fetch(url, options);

    // Si el token expiró (401 Unauthorized), envía al login
    if (response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
    }
    return response;
}

// ------------------------------
// 1) Cargar la lista de paquetes
// ------------------------------
async function cargarPaquetes() {
    const tablaBody = document.querySelector('#tabla-paquetes tbody');
    const errorDiv = document.getElementById('paquetes-error');
    tablaBody.innerHTML = '';
    errorDiv.textContent = '';

    try {
        const res = await fetchWithAuth(`${API_BASE}/paquetes/`);
        if (!res.ok) {
            const err = await res.json();
            errorDiv.textContent = err.detail || 'Error al obtener paquetes.';
            return;
        }
        const paquetes = await res.json();
        paquetes.forEach(paquete => {
            // Crea una fila por cada paquete
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${paquete.id}</td>
                <td>${paquete.cliente_destinatario.username}</td>
                <td>${paquete.peso}</td>
                <td>${paquete.dimensiones}</td>
                <td>${paquete.estado_actual ? paquete.estado_actual.nombre : 'Sin estado'}</td>
                <td>
                    <button class="btn-ver-historial" data-id="${paquete.id}">Ver Historial</button>
                </td>
            `;
            tablaBody.appendChild(tr);
        });
        // Asignar escuchadores a los botones “Ver Historial”
        document.querySelectorAll('.btn-ver-historial').forEach(btn => {
            btn.addEventListener('click', () => {
                const paqueteId = btn.getAttribute('data-id');
                mostrarHistorial(paqueteId);
            });
        });
    } catch (err) {
        console.error(err);
        errorDiv.textContent = 'Error de conexión al cargar paquetes.';
    }
}

// ------------------------------------
// 2) Cargar la lista de conductores
// ------------------------------------
async function cargarConductores() {
    const lista = document.getElementById('lista-conductores');
    const errorDiv = document.getElementById('conductores-error');
    lista.innerHTML = '';
    errorDiv.textContent = '';

    try {
        const res = await fetchWithAuth(`${API_BASE}/usuarios/conductores/`);
        if (!res.ok) {
            const err = await res.json();
            errorDiv.textContent = err.detail || 'Error al obtener conductores.';
            return;
        }
        const conductores = await res.json();
        conductores.forEach(c => {
            const li = document.createElement('li');
            li.textContent = `${c.id} — ${c.username} (${c.email})`;
            lista.appendChild(li);
        });
    } catch (err) {
        console.error(err);
        errorDiv.textContent = 'Error de conexión al cargar conductores.';
    }
}

// --------------------------------------------------
// 3) Crear un nuevo paquete (cliente autenticado)
// --------------------------------------------------
async function crearPaquete(event) {
    event.preventDefault();
    const errorDiv = document.getElementById('crear-paquete-error');
    const successDiv = document.getElementById('crear-paquete-success');
    errorDiv.textContent = '';
    successDiv.textContent = '';

    const destinatario = document.getElementById('destinatario').value;
    const peso = document.getElementById('peso').value;
    const dimensiones = document.getElementById('dimensiones').value;

    try {
        const res = await fetchWithAuth(`${API_BASE}/paquetes/`, {
            method: 'POST',
            body: JSON.stringify({
                cliente_destinatario: parseInt(destinatario),
                peso: parseFloat(peso),
                dimensiones: dimensiones
            })
        });
        if (res.status === 201 || res.status === 200) {
            successDiv.textContent = 'Paquete creado con éxito.';
            // Limpiar formulario y recargar la lista
            document.getElementById('crear-paquete-form').reset();
            cargarPaquetes();
        } else {
            const err = await res.json();
            errorDiv.textContent = err.detail || 'Error al crear paquete.';
        }
    } catch (err) {
        console.error(err);
        errorDiv.textContent = 'Error de conexión al crear paquete.';
    }
}

// --------------------------------------------------
// 4) Mostrar historial de un paquete en #tabla-historial
// --------------------------------------------------
async function mostrarHistorial(paqueteId) {
    const errorDiv = document.getElementById('historial-error');
    const tablaHist = document.querySelector('#tabla-historial tbody');
    errorDiv.textContent = '';
    tablaHist.innerHTML = '';

    if (!paqueteId) {
        errorDiv.textContent = 'Debes ingresar un ID de paquete.';
        return;
    }

    try {
        const res = await fetchWithAuth(`${API_BASE}/paquetes/${paqueteId}/historial/`);
        if (!res.ok) {
            const err = await res.json();
            errorDiv.textContent = err.detail || 'Error al obtener historial.';
            return;
        }
        const historial = await res.json();
        if (historial.length === 0) {
            errorDiv.textContent = 'Este paquete no tiene historial.';
            return;
        }
        historial.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${item.id}</td>
                <td>${item.estado.nombre}</td>
                <td>${new Date(item.fecha).toLocaleString()}</td>
                <td>${item.actualizador.username}</td>
            `;
            tablaHist.appendChild(tr);
        });
    } catch (err) {
        console.error(err);
        errorDiv.textContent = 'Error de conexión al cargar historial.';
    }
}

// --------------------------------------------------
// 5) Al cargar la página panel.html, inicializamos
// --------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    // Si no hay token en localStorage, redirige al login
    if (!getAccessToken()) {
        window.location.href = '/';
        return;
    }

    // Carga inicial de paquetes y conductores
    cargarPaquetes();
    cargarConductores();

    // Asignar manejador al formulario de creación de paquete
    const formCrearPaquete = document.getElementById('crear-paquete-form');
    if (formCrearPaquete) {
        formCrearPaquete.addEventListener('submit', crearPaquete);
    }

    // Asignar manejador al botón “Ver Historial”
    const btnVerHistorial = document.getElementById('ver-historial-btn');
    if (btnVerHistorial) {
        btnVerHistorial.addEventListener('click', () => {
            const paqueteId = document.getElementById('paquete-historial').value;
            mostrarHistorial(paqueteId);
        });
    }
});
