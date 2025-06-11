import { protectRoute } from './auth.js';
import { getCookie } from './utils.js';

// Esperar a que el DOM esté listo y luego verificar la sesión
document.addEventListener('DOMContentLoaded', async function() {
    await protectRoute();
    // Elementos de la interfaz
    const tabUsuarios = document.getElementById('tab-usuarios');
    const tabPaquetes = document.getElementById('tab-paquetes');
    const tabEstadisticas = document.getElementById('tab-estadisticas');
    const usuariosSection = document.getElementById('usuarios-section');
    const paquetesSection = document.getElementById('paquetes-section');
    const estadisticasSection = document.getElementById('estadisticas-section');
    const logoutBtn = document.getElementById('logout-btn');
    const nuevoUsuarioBtn = document.getElementById('nuevo-usuario-btn');
    const nuevoPaqueteBtn = document.getElementById('nuevo-paquete-btn');
    const editarSedeBtn = document.getElementById('editar-sede-btn');
    const filtroEstado = document.getElementById('filtro-estado');
    const aplicarFiltroBtn = document.getElementById('aplicar-filtro');
    
    // Tablas
    const usuariosTable = document.querySelector('#usuarios-table tbody');
    const paquetesTable = document.querySelector('#paquetes-table tbody');
    
    // Modales
    const asignarConductorModal = new bootstrap.Modal(document.getElementById('asignarConductorModal'));
    const nuevoUsuarioModal = new bootstrap.Modal(document.getElementById('nuevoUsuarioModal'));
    const nuevoPaqueteModal = new bootstrap.Modal(document.getElementById('nuevoPaqueteModal'));
    const sedeModal = new bootstrap.Modal(document.getElementById('sedeModal'));
    
    // Variables de estado
    let usuarios = [];
    let paquetes = [];
    let conductores = [];
    let clientes = [];

    // Mapa para seleccionar coordenadas del paquete
    let map;
    let marker;
    let mapInitialized = false;
    let sedeMap;
    let sedeMarker;
    let sedeMapInitialized = false;
    
    // Funciones de navegación
    tabUsuarios.addEventListener('click', () => {
        showSection('usuarios');
        loadUsuarios();
    });
    
    tabPaquetes.addEventListener('click', () => {
        showSection('paquetes');
        loadPaquetes();
    });
    
    tabEstadisticas.addEventListener('click', () => {
        showSection('estadisticas');
        loadEstadisticas();
    });
    
    function showSection(section) {
        usuariosSection.style.display = 'none';
        paquetesSection.style.display = 'none';
        estadisticasSection.style.display = 'none';
        
        tabUsuarios.classList.remove('active');
        tabPaquetes.classList.remove('active');
        tabEstadisticas.classList.remove('active');
        
        if (section === 'usuarios') {
            usuariosSection.style.display = 'block';
            tabUsuarios.classList.add('active');
        } else if (section === 'paquetes') {
            paquetesSection.style.display = 'block';
            tabPaquetes.classList.add('active');
        } else if (section === 'estadisticas') {
            estadisticasSection.style.display = 'block';
            tabEstadisticas.classList.add('active');
        }
    }
    
    // Cargar datos
    function loadUsuarios() {
        fetch('/api/admin/usuarios/')
            .then(response => response.json())
            .then(data => {
                usuarios = data;
                renderUsuarios();
            })
            .catch(error => console.error('Error:', error));
    }
    
    function loadPaquetes(estado = '') {
        let url = '/api/admin/paquetes/';
        if (estado) {
            url += `?estado=${estado}`;
        }
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                paquetes = data;
                renderPaquetes();
            })
            .catch(error => console.error('Error:', error));
    }
    
    function loadEstadisticas() {
        fetch('/api/admin/estadisticas/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('total-usuarios').textContent = data.usuarios_total;
                document.getElementById('total-paquetes').textContent = data.paquetes_total;
                document.getElementById('paquetes-pendientes').textContent = data.paquetes_pendientes;
                document.getElementById('paquetes-en-ruta').textContent = data.paquetes_en_ruta;
                document.getElementById('paquetes-entregados').textContent = data.paquetes_entregados;
            })
            .catch(error => console.error('Error:', error));
    }
    
    function loadConductores() {
        fetch('/api/admin/conductores/')
            .then(response => response.json())
            .then(data => {
                conductores = data;
                renderSelectConductores();
            })
            .catch(error => console.error('Error:', error));
    }

    function loadClientes() {
        fetch('/api/admin/usuarios/', {
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                clientes = data.filter(u => u.rol === 'cliente');
                renderSelectClientes();
            })
            .catch(error => console.error('Error:', error));
    }
    
    // Renderizar datos
    function renderUsuarios() {
        usuariosTable.innerHTML = '';
        usuarios.forEach(usuario => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${usuario.id}</td>
                <td>${usuario.username}</td>
                <td>${usuario.email || '-'}</td>
                <td>${usuario.rol}</td>
                <td>${usuario.activo ? 'Activo' : 'Inactivo'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary">Editar</button>
                    <button class="btn btn-sm btn-outline-danger">${usuario.activo ? 'Desactivar' : 'Activar'}</button>
                </td>
            `;
            usuariosTable.appendChild(row);
        });
    }
    
    function renderPaquetes() {
        paquetesTable.innerHTML = '';
        paquetes.forEach(paquete => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${paquete.id}</td>
                <td>${paquete.cliente}</td>
                <td>${paquete.conductor || 'Sin asignar'}</td>
                <td>${paquete.direccion_destino}</td>
                <td>
                    <span class="badge ${getEstadoBadgeClass(paquete.estado)}">
                        ${getEstadoText(paquete.estado)}
                    </span>
                </td>
                <td>${new Date(paquete.fecha_creacion).toLocaleString()}</td>
                <td>
                    ${paquete.estado !== 'entregado' && !paquete.conductor ? 
                        `<button class="btn btn-sm btn-primary asignar-btn" data-id="${paquete.id}">Asignar</button>` : 
                        '<button class="btn btn-sm btn-secondary" disabled>Asignar</button>'}
                </td>
            `;
            paquetesTable.appendChild(row);
        });
        
        // Agregar eventos a los botones de asignar
        document.querySelectorAll('.asignar-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const paqueteId = this.getAttribute('data-id');
                document.getElementById('paquete-id-asignar').value = paqueteId;
                loadConductores();
                asignarConductorModal.show();
            });
        });
    }
    
    function renderSelectConductores() {
        const select = document.getElementById('select-conductor');
        select.innerHTML = '<option value="">Seleccionar conductor</option>';
        conductores.forEach(conductor => {
            const option = document.createElement('option');
            option.value = conductor.id;
            option.textContent = conductor.username;
            select.appendChild(option);
        });
    }

    function renderSelectClientes() {
        const select = document.getElementById('select-cliente');
        select.innerHTML = '<option value="">Seleccionar cliente</option>';
        clientes.forEach(cliente => {
            const option = document.createElement('option');
            option.value = cliente.id;
            option.textContent = cliente.username;
            select.appendChild(option);
        });
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
        fetch('/api/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include'
        })
        .then(() => {
            window.location.href = '/login';
        })
        .catch(error => console.error('Error:', error));
    });
    
    nuevoUsuarioBtn.addEventListener('click', function() {
        nuevoUsuarioModal.show();
    });

    nuevoPaqueteBtn.addEventListener('click', function() {
        loadClientes();
        nuevoPaqueteModal.show();

        if (!mapInitialized) {
            mapboxgl.accessToken = MAPBOX_TOKEN;
            map = new mapboxgl.Map({
                container: 'map-new-paquete',
                style: 'mapbox://styles/mapbox/streets-v11',
                center: [-70.6483, -33.4569],
                zoom: 12
            });

            map.on('click', function (e) {
                if (marker) {
                    marker.remove();
                }
                marker = new mapboxgl.Marker().setLngLat(e.lngLat).addTo(map);
                document.getElementById('paquete-lat').value = e.lngLat.lat;
                document.getElementById('paquete-lon').value = e.lngLat.lng;
                reverseGeocode(e.lngLat.lat, e.lngLat.lng, addr => {
                    document.getElementById('direccion-destino').value = addr;
                });
            });

            mapInitialized = true;
        }

    });

    editarSedeBtn.addEventListener('click', function() {
        fetch('/api/routes/sede/')
            .then(r => r.json())
            .then(data => {
                document.getElementById('direccion-sede').value = data.direccion;
                document.getElementById('sede-lat').value = data.latitud;
                document.getElementById('sede-lon').value = data.longitud;
                sedeModal.show();

                if (!sedeMapInitialized) {
                    mapboxgl.accessToken = MAPBOX_TOKEN;
                    sedeMap = new mapboxgl.Map({
                        container: 'map-sede',
                        style: 'mapbox://styles/mapbox/streets-v11',
                        center: [data.longitud, data.latitud],
                        zoom: 12
                    });

                    sedeMap.on('click', function (e) {
                        if (sedeMarker) {
                            sedeMarker.remove();
                        }
                        sedeMarker = new mapboxgl.Marker().setLngLat(e.lngLat).addTo(sedeMap);
                        document.getElementById('sede-lat').value = e.lngLat.lat;
                        document.getElementById('sede-lon').value = e.lngLat.lng;
                        reverseGeocode(e.lngLat.lat, e.lngLat.lng, addr => {
                            document.getElementById('direccion-sede').value = addr;
                        });
                    });

                    sedeMapInitialized = true;
                } else {
                    sedeMap.setCenter([data.longitud, data.latitud]);
                    if (sedeMarker) {
                        sedeMarker.remove();
                    }
                    sedeMarker = new mapboxgl.Marker().setLngLat([data.longitud, data.latitud]).addTo(sedeMap);
                }
            });
    });
    
    aplicarFiltroBtn.addEventListener('click', function() {
        loadPaquetes(filtroEstado.value);
    });
    
    document.getElementById('confirmar-asignacion').addEventListener('click', function() {
        const paqueteId = document.getElementById('paquete-id-asignar').value;
        const conductorId = document.getElementById('select-conductor').value;
        
        if (!conductorId) {
            alert('Selecciona un conductor');
            return;
        }
        
        fetch('/api/assignments/asignar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify({
                paquete_id: paqueteId,
                conductor_id: conductorId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                asignarConductorModal.hide();
                loadPaquetes(filtroEstado.value);
                showToast('Paquete asignado correctamente');
            }
        })
        .catch(error => console.error('Error:', error));
    });
    
    document.getElementById('confirmar-nuevo-usuario').addEventListener('click', function() {
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const rol = document.getElementById('rol').value;
        
        if (!username || !password || !rol) {
            alert('Completa los campos requeridos');
            return;
        }
        
        fetch('/api/users/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                rol: rol
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                nuevoUsuarioModal.hide();
                document.getElementById('form-nuevo-usuario').reset();
                loadUsuarios();
                showToast('Usuario creado correctamente');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('confirmar-nuevo-paquete').addEventListener('click', function() {
        const clienteId = document.getElementById('select-cliente').value;
        const direccion = document.getElementById('direccion-destino').value;
        const lat = document.getElementById('paquete-lat').value;
        const lon = document.getElementById('paquete-lon').value;

        if (!clienteId || !direccion || !lat || !lon) {
            alert('Completa los campos requeridos');
            return;
        }

        fetch('/api/packages/crear/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify({
                cliente_id: clienteId,
                direccion_destino: direccion,
                lat: lat,
                lon: lon
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                nuevoPaqueteModal.hide();
                document.getElementById('form-nuevo-paquete').reset();
                loadPaquetes(filtroEstado.value);
                showToast('Paquete creado correctamente');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('guardar-sede').addEventListener('click', function() {
        const direccion = document.getElementById('direccion-sede').value;
        const lat = document.getElementById('sede-lat').value;
        const lon = document.getElementById('sede-lon').value;

        if (!direccion || !lat || !lon) {
            alert('Completa los campos');
            return;
        }

        fetch('/api/routes/sede/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify({
                direccion: direccion,
                latitud: lat,
                longitud: lon
            })
        })
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                sedeModal.hide();
                showToast('Sede actualizada');
            }
        })
        .catch(err => console.error(err));
    });
    
    // Funciones auxiliares
    
    function showToast(message) {
        // Implementar toast de notificación
        alert(message); // Temporal
    }

    function reverseGeocode(lat, lon, callback) {
        fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${lon},${lat}.json?access_token=${MAPBOX_TOKEN}`)
            .then(r => r.json())
            .then(data => {
                if (data.features && data.features.length > 0) {
                    callback(data.features[0].place_name);
                }
            });
    }
    
    // Inicialización
    showSection('usuarios');
    loadUsuarios();
    loadEstadisticas();
});
