document.getElementById('nuevaTareaForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const descripcion = document.getElementById('descripcion').value;

    fetch('/tareas/nueva', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre, descripcion })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Recargar la página para mostrar la nueva tarea
            window.location.reload();
        } else {
            alert('Error al crear la tarea');
        }
    })
    .catch(error => console.error('Error:', error));
});