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


const fechaInput = document.getElementById('birthday');
const horaInput = document.getElementById('time');

// Añadir evento "change" al input de fecha
fechaInput.addEventListener('change', () => {
  const fechaSeleccionada = new Date(fechaInput.value);
  const hoy = new Date();
  
  // Validar que la fecha seleccionada sea mayor o igual a la fecha actual
  if (fechaSeleccionada < hoy) {
    fechaInput.setCustomValidity('La fecha debe ser mayor o igual a la fecha actual');
  } else {
    fechaInput.setCustomValidity('');
  }
});

// Añadir evento "change" al input de hora
horaInput.addEventListener('change', () => {
  const horaSeleccionada = horaInput.value;
  
  // Obtener las horas y minutos de la hora seleccionada
  const hora = parseInt(horaSeleccionada.substring(0, 2));
  const minutos = parseInt(horaSeleccionada.substring(3));
  
  // Validar que la hora seleccionada sea entre las 8am y las 7pm
  if (hora < 8 || hora > 19) {
    horaInput.setCustomValidity('La hora seleccionada no es válida');
    horaInput.classList.add('time-invalida');
  } else {
      horaInput.setCustomValidity('');
    horaInput.classList.remove('time-invalida');
  }
});
     
//*********calendrio******** */
const fechaHoraInput = document.getElementById("birthday-hora");
const submitBtn = document.getElementById("submit-btn");

fechaHoraInput.addEventListener("input", function() {
  const fechaHoraSeleccionada = new Date(fechaHoraInput.value);
  const horaSeleccionada = fechaHoraSeleccionada.getHours();

  // Verificar si la hora seleccionada es válida
  if (horaSeleccionada < 8 || horaSeleccionada > 19) {
    // Hora inválida: deshabilitar botón de submit y cambiar color de fondo del input
    submitBtn.disabled = true;
    fechaHoraInput.style.backgroundColor = "red";
  } else {
    // Hora válida: habilitar botón de submit y restaurar color de fondo del input
    submitBtn.disabled = false;
    fechaHoraInput.style.backgroundColor = "white";
  }
});