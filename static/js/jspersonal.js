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