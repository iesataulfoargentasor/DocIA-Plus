function montarDiapositivas() {
  document.querySelectorAll("[data-dia]").forEach(function (deck) {
    if (deck.getAttribute("data-dia-listo") === "1") {
      return;
    }
    var slides = Array.prototype.slice.call(deck.querySelectorAll(".dia-slide"));
    if (!slides.length) {
      return;
    }
    var indice = 0;
    var cuenta = deck.querySelector("[data-dia-count]");
    var anterior = deck.querySelector("[data-dia-prev]");
    var siguiente = deck.querySelector("[data-dia-next]");

    function mostrar(n) {
      indice = (n + slides.length) % slides.length;
      slides.forEach(function (slide, i) {
        var activa = i === indice;
        slide.classList.toggle("is-active", activa);
        slide.hidden = !activa;
      });
      if (cuenta) {
        cuenta.textContent = indice + 1 + " / " + slides.length;
      }
    }

    anterior.addEventListener("click", function () {
      mostrar(indice - 1);
    });
    siguiente.addEventListener("click", function () {
      mostrar(indice + 1);
    });
    deck.addEventListener("keydown", function (evento) {
      if (evento.key === "ArrowRight") {
        evento.preventDefault();
        mostrar(indice + 1);
      }
      if (evento.key === "ArrowLeft") {
        evento.preventDefault();
        mostrar(indice - 1);
      }
    });

    deck.tabIndex = 0;
    deck.classList.add("dia-ready");
    deck.setAttribute("data-dia-listo", "1");
    mostrar(0);
  });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(montarDiapositivas);
} else {
  document.addEventListener("DOMContentLoaded", montarDiapositivas);
}
