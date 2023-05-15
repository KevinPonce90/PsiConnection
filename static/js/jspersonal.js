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


// ------------------------------------------- Administrador ------------------------------------------- //
// ------------------------------------------- Administrador ------------------------------------------- //
// ------------------------------------------- Administrador ------------------------------------------- //

// ------------------------------------ Modificar datos administrador ------------------------------------ //
// Espera a que se haga clic en el botón "Modificar datos"
if (currentUrl == "/templates/admin/adm_adm.html") {
  console.log('Amin');
  $('a.btn-edit').click(function () {

    const form = document.querySelector('#editAdmin');
    const filaId = $(this).closest('tr').data('id');
    const fila = document.querySelector(`tr[data-id="${filaId}"]`);

    const idAd = form.querySelector('input[name="idAd"]');
    const Fnombre = form.querySelector('input[name="nombreAd"]');
    const FapellidoP = form.querySelector('input[name="apellidoPAd"]');
    const FapellidoM = form.querySelector('input[name="apellidoMAd"]');

    // Acceder a las celdas específicas por índice
    const celda0 = fila.cells[0]; // Primera celda
    const celda1 = fila.cells[1]; // Segunda celda
    const celda2 = fila.cells[2]; // Tercera celda


    // Obtener los valores de las celdas
    const valor0 = celda0.textContent;
    const valor1 = celda1.textContent;
    const valor2 = celda2.textContent;

    // ID del administrador a editar
    idAd.value = filaId

    Fnombre.value = valor0;
    FapellidoP.value = valor1;
    FapellidoM.value = valor2;
  });
  // ------------------------------------ End Modificar datos administrador ------------------------------------ //
  
  // ------------------------------------ Eliminar administrador ------------------------------------ //
  $('a.delete').click(function () {
    
    const form = document.querySelector('#deleteAdmin');
    const filaId = $(this).closest('tr').data('id');
    const fila = document.querySelector(`tr[data-id="${filaId}"]`);
    
    const idAd = form.querySelector('input[name="idAd"]');
    const Fnombre = form.querySelector('input[name="nombre"]');
    
    
    // Acceder a las celdas específicas por índice
    const celda0 = fila.cells[0]; // Primera celda
    const celda1 = fila.cells[1]; // Segunda celda
    
    
    // Obtener los valores de las celdas
    const valor0 = celda0.textContent + ' ' + celda1.textContent;
    // ID del administrador a editar
    idAd.value = filaId;
    Fnombre.value = valor0;
    Fnombre.size = Fnombre.value.length;
    
  });
}
  // ------------------------------------ End Eliminar administrador ------------------------------------ //

  // ------------------------------------------- End Administrador ------------------------------------------- //
  // ------------------------------------------- End Administrador ------------------------------------------- //
  // ------------------------------------------- End Administrador ------------------------------------------- //



  // ------------------------------------------- Supervisor ------------------------------------------- //
  // ------------------------------------------- Supervisor ------------------------------------------- //
  // ------------------------------------------- Supervisor ------------------------------------------- //

  // ------------------------------------ Modificar datos Supervisor ------------------------------------ //
  // Espera a que se haga clic en el botón "Modificar datos"
  
  if (currentUrl == "/templates/admin/adm_super.html") {
    console.log('Sup');
    $('a.btn-edit').click(function () {

      const form = document.querySelector('#editSup');
      const filaId = $(this).closest('tr').data('id');
      const fila = document.querySelector(`tr[data-id="${filaId}"]`);

      const id = form.querySelector('input[name="idSup"]');
      const FnombreSup = form.querySelector('input[name="nombreSup"]');
      const FapellidoPSup = form.querySelector('input[name="apellidoPSup"]');
      const FapellidoMSup = form.querySelector('input[name="apellidoMSup"]');

      // Acceder a las celdas específicas por índice
      const celda0 = fila.cells[0]; // Primera celda
      const celda1 = fila.cells[1]; // Segunda celda
      const celda2 = fila.cells[2]; // Tercera celda


      // Obtener los valores de las celdas
      const valor0 = celda0.textContent;
      const valor1 = celda1.textContent;
      const valor2 = celda2.textContent;

      // ID del administrador a editar
      id.value = filaId;

      FnombreSup.value = valor0;
      FapellidoPSup.value = valor1;
      FapellidoMSup.value = valor2;
    });
    // ------------------------------------ End Modificar datos Supervisor ------------------------------------ //
    
  // ------------------------------------ Eliminar Supervisor ------------------------------------ //
  $('a.delete').click(function () {
    
    const form = document.querySelector('#deleteSup');
    const table = document.querySelector('#SupTable');
    const filaId = $(this).closest('tr').data('id');
    const fila = document.querySelector(`tr[data-id="${filaId}"]`);
    
    const id = form.querySelector('input[name="idSup"]');
    const Fnombre = form.querySelector('input[name="nombre"]');

    // Acceder a las celdas específicas por índice
    const celda0 = fila.cells[0]; // Primera celda
    const celda1 = fila.cells[1]; // Segunda celda


    // Obtener los valores de las celdas
    const valor0 = celda0.textContent + ' ' + celda1.textContent;
    // ID del supervisor a editar
    id.value = filaId;
    Fnombre.value = valor0;
    Fnombre.size = Fnombre.value.length;
    
  });
}
// ------------------------------------ End Eliminar Supervisor ------------------------------------ //

// ------------------------------------------- End Supervisor ------------------------------------------- //
// ------------------------------------------- End Supervisor ------------------------------------------- //
// ------------------------------------------- End Supervisor ------------------------------------------- //



  // ------------------------------------------- Practicante ------------------------------------------- //
  // ------------------------------------------- Practicante ------------------------------------------- //
  // ------------------------------------------- Practicante ------------------------------------------- //

  // ------------------------------------ Modificar datos practicante ------------------------------------ //
  // Espera a que se haga clic en el botón "Modificar datos"
  
  if (currentUrl == "/templates/admin/adm_pract.html") {
    console.log('Prac');
    $('a.btn-edit').click(function () {

      const form = document.querySelector('#editPrac');
      const filaId = $(this).closest('tr').data('id');
      const fila = document.querySelector(`tr[data-id="${filaId}"]`);

      const id = form.querySelector('input[name="idPrac"]');
      const FnombrePrac = form.querySelector('input[name="nombrePrac"]');
      const FapellidoPPrac = form.querySelector('input[name="apellidoPPrac"]');
      const FapellidoMPrac = form.querySelector('input[name="apellidoMPrac"]');

      // Acceder a las celdas específicas por índice
      const celda0 = fila.cells[0]; // Primera celda
      const celda1 = fila.cells[1]; // Segunda celda
      const celda2 = fila.cells[2]; // Tercera celda

      // Obtener los valores de las celdas
      const valor0 = celda0.textContent;
      const valor1 = celda1.textContent;
      const valor2 = celda2.textContent;

      // ID del administrador a editar
      id.value = filaId;

      FnombrePrac.value = valor0;
      FapellidoPPrac.value = valor1;
      FapellidoMPrac.value = valor2;
    });
    // ------------------------------------ End Modificar datos practicante  ------------------------------------ //
    
  // ------------------------------------ Eliminar practicante  ------------------------------------ //
  $('a.delete').click(function () {
    
    const form = document.querySelector('#deletePrac');
    const filaId = $(this).closest('tr').data('id');
    const fila = document.querySelector(`tr[data-id="${filaId}"]`);
    
    const id = form.querySelector('input[name="idPrac"]');
    const Fnombre = form.querySelector('input[name="nombre"]');

    // Acceder a las celdas específicas por índice
    const celda0 = fila.cells[0]; // Primera celda
    const celda1 = fila.cells[1]; // Segunda celda

    // Obtener los valores de las celdas
    const valor0 = celda0.textContent + ' ' + celda1.textContent;
    // ID del supervisor a editar
    id.value = filaId;
    Fnombre.value = valor0;
    Fnombre.size = Fnombre.value.length;
    
  });
}
// ------------------------------------ End Eliminar practicante  ------------------------------------ //

// ------------------------------------------- End practicante  ------------------------------------------- //
// ------------------------------------------- End practicante  ------------------------------------------- //
// ------------------------------------------- End practicante  ------------------------------------------- //




  // ------------------------------------------- Paciente ------------------------------------------- //
  // ------------------------------------------- Paciente ------------------------------------------- //
  // ------------------------------------------- Paciente ------------------------------------------- //

  // ------------------------------------ Modificar datos Paciente ------------------------------------ //
  // Espera a que se haga clic en el botón "Modificar datos"
  
  if (currentUrl == "/templates/admin/adm_pacie.html") {
    console.log('Paci');
    $('a.btn-edit').click(function () {

      const form = document.querySelector('#editPaci');
      const filaId = $(this).closest('tr').data('id');
      const fila = document.querySelector(`tr[data-id="${filaId}"]`);

      const id = form.querySelector('input[name="idPaci"]');
      const FnombrePac = form.querySelector('input[name="nombrePaci"]');
      const FapellidoPPac = form.querySelector('input[name="apellidoPPaci"]');
      const FapellidoMPac = form.querySelector('input[name="apellidoMPaci"]');

      // Acceder a las celdas específicas por índice
      const celda0 = fila.cells[0]; // Primera celda
      const celda1 = fila.cells[1]; // Segunda celda
      const celda2 = fila.cells[2]; // Tercera celda

      // Obtener los valores de las celdas
      const valor0 = celda0.textContent;
      const valor1 = celda1.textContent;
      const valor2 = celda2.textContent;

      // ID del Paciente a editar
      id.value = filaId;

      FnombrePac.value = valor0;
      FapellidoPPac.value = valor1;
      FapellidoMPac.value = valor2;
    });
    // ------------------------------------ End Modificar datos Paciente  ------------------------------------ //
    
  // ------------------------------------ Eliminar Paciente  ------------------------------------ //
  $('a.delete').click(function () {
    
    const form = document.querySelector('#deletePaci');
    const filaId = $(this).closest('tr').data('id');
    const fila = document.querySelector(`tr[data-id="${filaId}"]`);
    
    const id = form.querySelector('input[name="idPaci"]');
    const Fnombre = form.querySelector('input[name="nombre"]');

    // Acceder a las celdas específicas por índice
    const celda0 = fila.cells[0]; // Primera celda
    const celda1 = fila.cells[1]; // Segunda celda

    // Obtener los valores de las celdas
    const valor0 = celda0.textContent + ' ' + celda1.textContent;
    // ID del Paciente a editar
    id.value = filaId;
    Fnombre.value = valor0;
    Fnombre.size = Fnombre.value.length;
  });
}
// ------------------------------------ End Eliminar Paciente  ------------------------------------ //

// ------------------------------------------- End Paciente  ------------------------------------------- //
// ------------------------------------------- End Paciente  ------------------------------------------- //
// ------------------------------------------- End Paciente  ------------------------------------------- //


// ----------------------------------------- Contraseñas ----------------------------------------- //

function checkPasswordMatch1() { //administrador
  var password = document.getElementById("contraAd").value;
  var confirmPassword = document.getElementById("confirmPassword").value;
  
  if (password !== confirmPassword) {
    document.getElementById("confirmPassword").setCustomValidity("Las contraseñas no coinciden");
  } else {
    document.getElementById("confirmPassword").setCustomValidity("");
  }
}

function checkPasswordMatch() { //supervisor
  var password = document.getElementById("contraSup").value;
  var confirmPassword = document.getElementById("confirmPasswordSu").value;
  
  if (password !== confirmPassword) {
    document.getElementById("confirmPasswordSu").setCustomValidity("Las contraseñas no coinciden");
  } else {
    document.getElementById("confirmPasswordSu").setCustomValidity("");
  }
}

// ----------------------------------------- End Contraseñas ----------------------------------------- //