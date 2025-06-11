import { protectRoute } from './auth.js';

// Esperar a que el DOM esté listo para luego verificar la sesión
document.addEventListener('DOMContentLoaded', async function() {
    await protectRoute();
    const mensajeError = document.getElementById('mensaje-error');

    fetch('/api/packages/mis-pedidos/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) throw new Error('Error al obtener paquetes');
        return response.json();
    })
    .then(data => {
        const tbody = document.querySelector('#tabla-paquetes tbody');
        data.forEach(p => {
            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td>${p.id}</td>
                <td>${p.direccion_destino}</td>
                <td>
                    <span class="badge ${getEstadoBadgeClass(p.estado)}">
                        ${getEstadoText(p.estado)}
                    </span>
                </td>
                <td>${new Date(p.fecha_creacion).toLocaleString()}</td>
                <td>${p.conductor ?? 'No asignado'}</td>
            `;
            tbody.appendChild(fila);
        });
    })
    .catch(err => {
        mensajeError.textContent = err.message;
        mensajeError.classList.remove('d-none');
    });
});

function getEstadoText(estado) {
    const estados = {
        'pendiente': 'Pendiente',
        'en_ruta': 'En ruta',
        'entregado': 'Entregado'
    };
    return estados[estado] || estado;
}

function getEstadoBadgeClass(estado) {
    const clases = {
        'pendiente': 'bg-warning',
        'en_ruta': 'bg-info',
        'entregado': 'bg-success'
    };
    return clases[estado] || 'bg-secondary';
}
