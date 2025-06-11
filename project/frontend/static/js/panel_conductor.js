import { protectRoute } from './auth.js';
import { getCookie } from './utils.js';

// Esperar a que el DOM esté listo y luego verificar la sesión
document.addEventListener('DOMContentLoaded', async function() {
    await protectRoute();
    // Elementos de la interfaz
    const logoutBtn = document.getElementById('logout-btn');
    const paquetesTable = document.querySelector('#paquetes-table tbody');
    const cambiarEstadoModal = new bootstrap.Modal(document.getElementById('cambiarEstadoModal'));
    const crearRutaBtn = document.getElementById('crear-ruta-btn');
    const distanciaInfo = document.getElementById('distancia-info');
    const duracionInfo = document.getElementById('duracion-info');
    const infoPanel = document.getElementById('info-panel');
    let map;
    let routeLayer;
    let markerLayer;
    
    // Variables de estado
    let paquetes = [];
    
    // Cargar datos
    function loadPaquetes() {
        fetch('/api/packages/mis-paquetes/')
            .then(response => response.json())
            .then(data => {
                paquetes = data;
                renderPaquetes();
                updateStats();
            })
            .catch(error => console.error('Error:', error));
    }
    
    // Renderizar datos
    function renderPaquetes() {
        paquetesTable.innerHTML = '';
        paquetes.forEach(paquete => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><input type="checkbox" class="seleccionar-paquete" value="${paquete.id}"></td>
                <td>${paquete.id}</td>
                <td>${paquete.cliente}</td>
                <td>${paquete.direccion_destino}</td>
                <td>
                    <span class="badge ${getEstadoBadgeClass(paquete.estado)}">
                        ${getEstadoText(paquete.estado)}
                    </span>
                </td>
                <td>${new Date(paquete.fecha_creacion).toLocaleDateString()}</td>
                <td>
                    <button class="btn btn-sm btn-primary cambiar-estado-btn" data-id="${paquete.id}">
                        Cambiar Estado
                    </button>
                </td>
            `;
            paquetesTable.appendChild(row);
        });
        
        // Agregar eventos a los botones de cambiar estado
        document.querySelectorAll('.cambiar-estado-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const paqueteId = this.getAttribute('data-id');
                const paquete = paquetes.find(p => p.id == paqueteId);
                
                document.getElementById('paquete-id-cambiar').value = paqueteId;
                document.getElementById('select-estado').value = paquete.estado;
                cambiarEstadoModal.show();
            });
        });
    }
    
    function updateStats() {
        document.getElementById('total-paquetes').textContent = paquetes.length;
        document.getElementById('en-ruta').textContent = paquetes.filter(p => p.estado === 'en_ruta').length;
        document.getElementById('entregados').textContent = paquetes.filter(p => p.estado === 'entregado').length;
    }
    
    // Funciones auxiliares
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
    
    
    // Eventos
    logoutBtn.addEventListener('click', function() {
        // Implementar lógica de logout
        window.location.href = '/login';
    });
    
    document.getElementById('confirmar-cambio-estado').addEventListener('click', function() {
        const paqueteId = document.getElementById('paquete-id-cambiar').value;
        const nuevoEstado = document.getElementById('select-estado').value;
        
        fetch(`/api/packages/${paqueteId}/estado/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                estado: nuevoEstado
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                cambiarEstadoModal.hide();
                loadPaquetes();
                alert('Estado actualizado correctamente');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    crearRutaBtn.addEventListener('click', function() {
        const seleccionados = Array.from(document.querySelectorAll('.seleccionar-paquete:checked'))
            .map(cb => parseInt(cb.value));

        if (seleccionados.length === 0) {
            alert('Selecciona al menos un paquete');
            return;
        }

        const paquetesSeleccionados = paquetes.filter(p => seleccionados.includes(p.id));

        fetch('/api/routes/sede/')
            .then(r => r.json())
            .then(sede => {
                return fetch('/api/routes/crear/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        sede: sede.direccion,
                        paquetes: seleccionados
                    })
                }).then(resp => resp.json())
                  .then(data => ({ data, sede, paquetesSeleccionados }));
            })
            .then(({ data, sede, paquetesSeleccionados }) => {
                if (data.geometry) {
                    mostrarRuta(data.geometry, sede, paquetesSeleccionados);
                    mostrarInfoRuta(data);
                } else if (data.error) {
                    alert(data.error);
                }
            })
            .catch(error => console.error('Error:', error));
    });

    function initMap() {
        if (!map) {
            map = L.map('map').setView([-33.45, -70.66], 12);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);
        }
    }

    function mostrarRuta(geojson, sede, paquetesSeleccionados) {
        initMap();
        if (routeLayer) {
            map.removeLayer(routeLayer);
        }
        if (markerLayer) {
            map.removeLayer(markerLayer);
        }
        routeLayer = L.geoJSON(geojson).addTo(map);
        markerLayer = L.layerGroup().addTo(map);

        // Sede en azul
        L.circleMarker([sede.latitud, sede.longitud], {
            color: 'blue',
            radius: 6
        }).addTo(markerLayer).bindPopup('Sede');

        paquetesSeleccionados.forEach((p, idx) => {
            L.circleMarker([p.latitud, p.longitud], {
                color: 'red',
                radius: 6
            }).addTo(markerLayer).bindPopup(`Paquete ${p.id}`);
        });

        map.fitBounds(routeLayer.getBounds());
    }

    function mostrarInfoRuta(data) {
        const km = (data.distancia_total_m / 1000).toFixed(2);
        const minutos = (data.duracion_total_s / 60).toFixed(1);
        distanciaInfo.textContent = `${km} km`;
        duracionInfo.textContent = `${minutos} min`;
        infoPanel.style.display = 'flex';
    }
    
    // Inicialización
    initMap();
    loadPaquetes();
});
