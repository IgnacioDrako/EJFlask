document.addEventListener('DOMContentLoaded', function() {
    Swal.fire({
        title: 'Necesitas permisos CRACK!',
        text: 'Esta página solo puede ser vista por administradores.',
        imageUrl: '../static/img/cat.gif',
        imageWidth: 400,
        imageHeight: 200,
        imageAlt: 'Custom image',
        confirmButtonText: 'Entendido',
        background: '#111',
    });
});