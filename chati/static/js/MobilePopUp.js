function toggleMobilePopup(event) {
  event.preventDefault(); 
  const popup = document.getElementById("MobilePopup");
  const homeicon = document.getElementById("LogInHomeIcon");
  const isMobile = window.matchMedia("(max-width: 768px)").matches;
  if (isMobile) {
    popup.classList.toggle("hidden");
    try{
      homeicon.setAttribute("href", "#");
    } catch{}
    
  }
}

window.addEventListener("resize", () => {
  const homeicon = document.getElementById("LogInHomeIcon");
  const popup = document.getElementById("MobilePopup");
  const isDesktop = window.innerWidth > 768;

  if (isDesktop) {
    const feedURL = homeicon?.dataset?.feed;
    if (homeicon && feedURL) {
      homeicon.setAttribute("href", feedURL);
    }

    if (popup && !popup.classList.contains("hidden")) {
      popup.classList.add("hidden");
      console.log("Popup ocultado por resize en escritorio");
    }
  }
});

