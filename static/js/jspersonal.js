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
///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////
///Hora y fecha

// const fechaInput = document.getElementById('fecha');
// const horaInput = document.getElementById('hora');

// // Añadir evento "change" al input de fecha
// fechaInput.addEventListener('change', () => {
//   const fechaSeleccionada = new Date(fechaInput.value);
//   const hoy = new Date();
  
//   // Validar que la fecha seleccionada sea mayor o igual a la fecha actual
//   if (fechaSeleccionada < hoy) {
//     fechaInput.setCustomValidity('La fecha debe ser mayor o igual a la fecha actual');
//   } else {
//     fechaInput.setCustomValidity('');
//   }
// });

// // Añadir evento "change" al input de hora
// horaInput.addEventListener('change', () => {
//   const horaSeleccionada = horaInput.value;
  
//   // Obtener las horas y minutos de la hora seleccionada
//   const hora = parseInt(horaSeleccionada.substring(0, 2));
//   const minutos = parseInt(horaSeleccionada.substring(3));
  
//   // Validar que la hora seleccionada sea entre las 8am y las 7pm
//   if (hora < 8 || hora > 19) {
//     horaInput.setCustomValidity('La hora seleccionada no es válida');
//     horaInput.classList.add('hora-invalida');
//   } else {
//       horaInput.setCustomValidity('');
//     horaInput.classList.remove('hora-invalida');
//   }
// });
     

// const fechaHoraInput = document.getElementById("fecha-hora");
// const submitBtn = document.getElementById("submit-btn");

// fechaHoraInput.addEventListener("input", function() {
//   const fechaHoraSeleccionada = new Date(fechaHoraInput.value);
//   const horaSeleccionada = fechaHoraSeleccionada.getHours();

//   // Verificar si la hora seleccionada es válida
//   if (horaSeleccionada < 8 || horaSeleccionada > 19) {
//     // Hora inválida: deshabilitar botón de submit y cambiar color de fondo del input
//     submitBtn.disabled = true;
//     fechaHoraInput.style.backgroundColor = "red";
//   } else {
//     // Hora válida: habilitar botón de submit y restaurar color de fondo del input
//     submitBtn.disabled = false;
//     fechaHoraInput.style.backgroundColor = "white";
//   }
// });
///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////
//    Tranferir datos a modal Administrador

// Obtener la tabla y el modal
// var table = document.getElementById("AdminTable");
// var modal = document.getElementById("editEmployeeModal");

// // Obtener los elementos del formulario
// var nombreInput    = document.getElementById("nombreAd");
// var apellidoPInput = document.getElementById("apellidoPAd");
// var apellidoMInput = document.getElementById("apellidoMAd");
// var correoInput    = document.getElementById("correoAd");

// // Función para abrir el modal y llenar el formulario
// function editar(button) {
//   // Obtener la fila de la tabla
//   var row = button.parentNode.parentNode;
//   // Obtener los valores de las celdas
//   var nombre    = row.cells[0].innerHTML;
//   var apellidoP = row.cells[1].innerHTML;
//   var apellidoM = row.cells[2].innerHTML;
//   var correo    = row.cells[3].innerHTML;
//   // Llenar el formulario con los valores de las celdas
//   nombreInput.value      = nombre;
//   apellidoPInput.value   = apellidoP;
//   apellidoMInput.value   = apellidoM;
//   correoInput.value      = correo;
//   // Mostrar el modal
//   modal.style.display = "block";
// }

// // Función para guardar los cambios
// function guardar() {
//   // Obtener los valores del formulario
//   var nombre    = nombreInput.value;
//   var apellidoP = apellidoPInput.value;
//   var apellidoM = apellidoMInput.value;
//   var correo    = correoInput.value;
//   // Actualizar la fila de la tabla con los nuevos valores
//   var row = table.getElementsByTagName("tr")[1];
//   row.cells[0].innerHTML = nombre;
//   row.cells[1].innerHTML = apellidoP;
//   row.cells[2].innerHTML = apellidoM;
//   row.cells[3].innerHTML = correo;
//   // Cerrar el modal
//   modal.style.display = "none";
// }

// // Función para cerrar el modal
// var span = document.getElementsByClassName("btn-close")[0];
// span.onclick = function() {
//   modal.style.display = "none";
// }






// var table = document.getElementById("AdminTable");
// var form = document.getElementById("editAdmin");

// // Agregar un evento "click" a cada fila de la tabla
// for (var i = 0; i < table.rows.length; i++) {
//   table.rows[i].addEventListener("click", function() {
//     // Obtener los datos de la fila seleccionada
//     var nombre = this.cells[0].innerHTML;
//     var apellidoP = this.cells[1].innerHTML;
//     var apellidoM = this.cells[2].innerHTML;
//     var correo = this.cells[3].innerHTML;

//     // Asignar los datos a los campos del formulario
//     form.elements["nombreAd"].value    = nombre;
//     form.elements["apellidoPAd"].value = apellidoP;
//     form.elements["apellidoMAd"].value = apellidoM;
//     form.elements["correoAd"].value    = correo;
//   });
// }






// Obtener elementos de la tabla y del formulario
const tabla = document.getElementById("AdminTable");
const form = document.querySelector("#editEmployeeModal form");
const nombreInput = form.querySelector("#nombreAd");
const apellidoPInput = form.querySelector("#apellidoPAd");
const apellidoMInput = form.querySelector("#apellidoMAd");
const correoInput = form.querySelector("#correoAd");


// Función para mostrar el modal y transferir los datos de la fila correspondiente
function mostrarFormulario(boton) {
  // Obtener la fila correspondiente al botón presionado
  const fila = boton.closest("tr");
  
  // Obtener los datos de la fila y asignarlos a los campos del formulario
  const nombre    = fila.querySelector("td:nth-child(1)").textContent;
  const apellidoP = fila.querySelector("td:nth-child(2)").textContent;
  const apellidoM = fila.querySelector("td:nth-child(3)").textContent;
  const correo    = fila.querySelector("td:nth-child(4)").textContent;
  
  nombreInput.value    = nombre;
  apellidoPInput.value = apellidoP;
  apellidoMInput.value = apellidoM;
  correoInput.value    = correo;


  // Mostrar el modal
  const modal = document.getElementById("editEmployeeModal");
  modal.style.display = "block";
}

// Cerrar el modal cuando se envíe el formulario
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const modal = document.getElementById("editEmployeeModal");
  modal.style.display = "none";
});