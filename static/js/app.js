window.addEventListener("DOMContentLoaded", function () {
    const btnLogin = document.getElementById("btnLogin");
    const btnRegistro = document.getElementById("btnRegistro");
    const btnEntrar = document.getElementById("btnEntrar");
    const btnCrear = document.getElementById("btnCrearUsuario");

    if (btnLogin) btnLogin.addEventListener("click", mostrarLogin);
    if (btnRegistro) btnRegistro.addEventListener("click", mostrarRegistro);
    if (btnEntrar) btnEntrar.addEventListener("click", login);
    if (btnCrear) btnCrear.addEventListener("click", crearUsuario);
});

function mostrarLogin() {
    document.getElementById("registroForm").classList.add("d-none");
    document.getElementById("loginForm").classList.remove("d-none");
    document.getElementById("loginForm").scrollIntoView({ behavior: "smooth" });
}

function mostrarRegistro() {
    document.getElementById("loginForm").classList.add("d-none");
    document.getElementById("registroForm").classList.remove("d-none");
    document.getElementById("registroForm").scrollIntoView({ behavior: "smooth" });
}

async function login() {
    const correo = document.getElementById('correo').value;
    const contrasena = document.getElementById('contrasena').value;
    const respuesta = document.getElementById("respuesta");

    try {
        const res = await fetch("/api/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ correo, contrasena })
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || "Error en la autenticación");
        }

        if (data.usuario.tipo_usuario === "admin") {
            window.location.href = "/panel/";
        } else {
            alert("Este sistema web es solo para administradores. Usa la app móvil.");
        }

    } catch (error) {
        respuesta.textContent = `❌ Error: ${error.message}`;
    }
}

async function crearUsuario() {
    const nombre = document.getElementById('nombreNuevo').value;
    const correo = document.getElementById('correoNuevo').value;
    const tipo = document.getElementById('rolNuevo').value;
    const contrasena = document.getElementById('claveNuevo').value;
    const respuesta = document.getElementById("respuesta");

    try {
        const res = await fetch("/api/registrar/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                nombre,
                correo,
                contrasena,
                tipo_usuario: tipo
            }),
        });

        const data = await res.json();

        if (res.ok) {
            respuesta.textContent = "✅ Usuario creado correctamente";
            document.getElementById("nombreNuevo").value = "";
            document.getElementById("correoNuevo").value = "";
            document.getElementById("rolNuevo").value = "cliente";
            document.getElementById("claveNuevo").value = "";
        } else {
            throw new Error(data.error || JSON.stringify(data));
        }
    } catch (error) {
        respuesta.textContent = "❌ Error: " + error.message;
    }
}
