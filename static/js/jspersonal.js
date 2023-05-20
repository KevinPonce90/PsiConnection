// Obtenemos la URL actual de la página
var currentUrl = window.location.pathname;
console.log(currentUrl);
// Obtenemos todos los enlaces de la barra de navegación
var navLinks = document.querySelectorAll('.nav-link.click-scroll');

// Iteramos por cada enlace y comparamos su URL con la URL actual de la página
for (var i = 0; i < navLinks.length; i++) {

  if (navLinks[i].getAttribute('href') == currentUrl) {
    // Si la URL del enlace coincide con la URL actual de la página, agregamos la clase 'active'
    navLinks[i].classList.add('active');


  }
}
// ------------------------------------ Cards index admin ------------------------------------ //
if (currentUrl == "/templates/admin/index_admin.html") {
  const cards = document.querySelectorAll('.Lcard');

  for (let i = 0; i < cards.length; i++) {
    const card = cards[i];

    card.addEventListener('mouseover', () => {
      setTimeout(() => {
        card.querySelector('.Ctexto').classList.toggle('display-none');
        card.querySelector('.CtextoHover').classList.toggle('display-block');
      }, 100);
    });

    card.addEventListener('mouseout', () => {
      setTimeout(() => {
        card.querySelector('.Ctexto').classList.toggle('display-none');
        card.querySelector('.CtextoHover').classList.toggle('display-block');
      }, 100);
    });
  }
}
// ------------------------------------ End Cards index admin ------------------------------------ //

// ------------------------------------ Agregar practicante ------------------------------------ //
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

// ------------------------------------ End Agregar practicante ------------------------------------ //


if (currentUrl == "/templates/paciente/agenda_cita.html") {

  // ---------------------------- Validacion fecha ---------------------------- //
  // Obtenemos la fecha actual
  var today = new Date().toISOString().split('T')[0];

  // Obtenemos el elemento del input de fecha
  var dateInput = document.getElementById('fecha');

  // Establecemos la fecha mínima permitida como la fecha actual
  dateInput.setAttribute('min', today);

  // ---------------------------- End Validacion fecha ---------------------------- //

  // ---------------------------- Validacion hora ---------------------------- //
  const timeInput = document.getElementById('time');

  timeInput.addEventListener('input', () => {
    const time = timeInput.value;
    const parts = time.split(':');
    timeInput.value = `${parts[0]}:00`;
  });

  const timeError = document.getElementById('time-error');


  timeInput.addEventListener('change', () => {
    const selectedTime = timeInput.value;
    const selectedHour = parseInt(selectedTime.split(':')[0], 10);

    if (selectedHour < 8 || selectedHour > 20) {
      timeInput.setCustomValidity('Elija una hora valida');
      timeInput.value = '';
      timeError.style.display = 'block';

      const optionElements = timeInput.querySelectorAll('option');
      optionElements.forEach(option => {
        const hour = parseInt(option.value.split(':')[0], 10);
        if (hour < 8 || hour > 20) {
          option.disabled = true;
        } else {
          option.disabled = false;
        }
      });
    } else {
      timeInput.setCustomValidity('');
      timeError.style.display = 'none';

      const optionElements = timeInput.querySelectorAll('option');
      optionElements.forEach(option => {
        option.disabled = false;
      });
    }
  });

  const form = document.getElementById('elegir');
  const modalidadSelect = document.getElementById('tipoCita');

  form.addEventListener("submit", (event) => {
    if (modalidadSelect.value === "") {
      event.preventDefault();
    }
  });
  //---------------------------- End Validacion hora ---------------------------- //

  // --------------------------- Modal agenda cita --------------------------- //
  $('a.link-card-practicante').click(function () {

    const form = document.querySelector('#elegir');
    const lista  = $(this).closest('a').data('id');
    
    const elemento = lista.split(',')

    const FcorreoPrac  = form.querySelector('input[name="correoPrac"]');
    const FidPrac     = form.querySelector('input[name="idPrac"]');

    // Asignacion correo
    FidPrac.value     = elemento[0];
    FcorreoPrac.value  = elemento[1];
  });
}
  // --------------------------- End Modal agenda cita --------------------------- //

// ------------------------------------ Modal eliminar cita practicante ------------------------------------ //
// if (currentUrl == "/indexPracticante") {
  $('a.delete').click(function () {

    const form = document.querySelector('#borrarCita');
    const cita = $(this).closest('tr').data('id');
    const fila = document.querySelector(`tr[data-id="${cita}"]`);

    const FidCita = form.querySelector('input[name="idCita"]');


    // Acceder a las celdas específicas por índice
    const celda0 = fila.cells[0]; // Primera celda
    const celda1 = fila.cells[1]; // Segunda celda


    // Obtener los valores de las celdas
    const valor0 = celda0.textContent + ' ' + celda1.textContent;
    // ID del administrador a editar
    FidCita.value = cita;
    document.getElementById('nombreModal').textContent = valor0;

  });
// }
// ------------------------------------ End Modal eliminar cita practicante ------------------------------------ //

