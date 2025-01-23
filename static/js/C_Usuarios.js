document.getElementById('nuevoUsuarioForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const correo = document.getElementById('correo').value;
    const contrasena = document.getElementById('contrasena').value;

    fetch('/usuarios/nuevo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre, correo, contrasena })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Recargar la página para mostrar el nuevo usuario
            window.location.reload();
        } else {
            alert('Error al crear el usuario');
        }
    })
    .catch(error => console.error('Error:', error));
});
