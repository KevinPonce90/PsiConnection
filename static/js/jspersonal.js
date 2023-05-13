// Obtenemos la URL actual de la página
var currentUrl = window.location.pathname;
// Obtenemos todos los enlaces de la barra de navegación
var navLinks = document.querySelectorAll('.nav-link.click-scroll');

// Iteramos por cada enlace y comparamos su URL con la URL actual de la página
for (var i = 0; i < navLinks.length; i++) {

    if (navLinks[i].getAttribute('href') == currentUrl) {
        // Si la URL del enlace coincide con la URL actual de la página, agregamos la clase 'active'
        navLinks[i].classList.add('active');


    }
}

if (currentUrl == "/templates/supervisor/agregar_practicante.html") {
    console.log(currentUrl);
    const editableInput = document.getElementById('input-editable');
    const readonlyInput = document.getElementById('input-readonly');
    const combinedInput = document.getElementById('correoPrac');

    // Función para combinar los valores de los dos inputs
    function combineInputs() {
        const editableValue = editableInput.value;
        const readonlyValue = readonlyInput.value;
        combinedInput.value = `${editableValue}${readonlyValue}`;
        console.log(combinedInput.value);
    }

    // Asignar el valor del input combinado antes de hacer el submit
    document.getElementById('agregarPacticante').addEventListener('submit', function (event) {
        combineInputs();
    });

    // Escuchar cambios en los dos inputs y actualizar el input combinado
    editableInput.addEventListener('input', combineInputs);
    readonlyInput.addEventListener('input', combineInputs);

    const formulario = document.getElementById('agregarPacticante');

    formulario.addEventListener('submit', function (event) {
        event.preventDefault(); // Evita que se realice el submit por defecto del formulario
    });
}
