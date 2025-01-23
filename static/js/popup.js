document.addEventListener('DOMContentLoaded', function() {
    // Crear un nuevo objeto de audio
    const audio = new Audio('../static/sounds/alert.mp3');
    // Reproducir el sonido cuando se muestra la alerta
    Swal.fire({
        title: 'Necesitas permisos CRACK!',
        text: 'Esta página solo puede ser vista por administradores.',
        imageUrl: '../static/img/cat.gif',
        imageWidth: 400,
        imageHeight: 200,
        imageAlt: 'Custom image',
        confirmButtonText: 'Entendido',
        background: '#111',
        didOpen: () => {
            audio.play();
        },
        willClose: () => {
            audio.pause();
            audio.currentTime = 0;
        }
    });
});