function toggleMobilePopup(event) {
  event.preventDefault(); // Detiene la navegación del <a>
  const popup = document.getElementById("MobilePopup");
  const homeicon = document.getElementById("LogInHomeIcon");
  const isMobile = window.matchMedia("(max-width: 768px)").matches;
  if (isMobile) {
    popup.classList.toggle("hidden");
    homeicon.setAttribute("href", "#");
  }
}

window.addEventListener("resize", () => {
  const popup = document.getElementById("MobilePopup");
  const homeicon = document.getElementById("LogInHomeIcon");
  const isDesktop = window.innerWidth > 768;

  if (isDesktop) {
    homeicon.setAttribute("href", "{% url 'feed' %}");
    // Seguridad: asegura que el popup esté oculto
    if (popup && !popup.classList.contains("hidden")) {
      popup.classList.add("hidden");
      console.log("Popup ocultado por resize en escritorio");
    }
  }
});
