function toggleMobilePopup() {
  const popup = document.getElementById("LPMobilePopup");
  const isMobile = window.matchMedia("(max-width: 768px)").matches;

  if (isMobile) {
    popup.classList.toggle("hidden");
  }
}
