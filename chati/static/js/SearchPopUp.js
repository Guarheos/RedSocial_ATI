document.addEventListener("DOMContentLoaded", () => {
    const searchIcon = document.getElementById("LogInSearchIcon");
    const popup = document.getElementById("popupSearch");
    const input = document.getElementById("userSearchInput");
    const ul = document.getElementById("searchResults");
    let debounceTimeout;

    if (!searchIcon || !popup || !input || !ul) {
        console.error("Faltan elementos necesarios en el DOM");
        return;
    }

    // 🔄 Toggle del popup y posicionamiento ajustado
    searchIcon.addEventListener("click", (event) => {
        event.preventDefault();

        if (popup.style.display === "block") {
            popup.style.display = "none";
        } else {
            const rect = searchIcon.getBoundingClientRect();
            const popupWidth = popup.offsetWidth || 250;
            const popupHeight = popup.offsetHeight || 180;

            let top = rect.bottom + window.scrollY + 18;
            let left = rect.left + (rect.width / 2) - (popupWidth / 2);

            if (left < 10) left = 10;
            if (left + popupWidth > window.innerWidth) {
                left = window.innerWidth - popupWidth - 10;
            }
            if (top + popupHeight > window.scrollY + window.innerHeight) {
                top = window.scrollY + window.innerHeight - popupHeight - 10;
            }

            popup.style.position = "absolute";
            popup.style.top = `${top}px`;
            popup.style.left = `${left}px`;
            popup.style.display = "block";
        }
    });

    // 🔒 Cierre del popup al hacer clic fuera
    document.addEventListener("click", (event) => {
        if (!popup.contains(event.target) && event.target !== searchIcon) {
            popup.style.display = "none";
        }
    });

    // 🔎 Búsqueda con debounce
    input.addEventListener("input", (event) => {
        const query = event.target.value.trim();
        clearTimeout(debounceTimeout);

        if (query.length < 2) {
            ul.innerHTML = "";
            return;
        }

        debounceTimeout = setTimeout(async () => {
            try {
                const response = await fetch(`/buscar_usuarios/?q=${encodeURIComponent(query)}`);
                const results = await response.json();
                ul.innerHTML = "";

                results.forEach(user => {
                    const li = document.createElement("li");

                    const img = document.createElement("img");
                    img.src = user.profile_pic || "/static/images/DefaultUser.png";
                    img.alt = `${user.username} avatar`;
                    img.classList.add("avatar-mini");

                    const link = document.createElement("a");
                    link.textContent = user.username;
                    link.href = `/feed/profile/${user.username}/`;
                    link.classList.add("search-result-link");

                    link.addEventListener("click", () => {
                        popup.style.display = "none";
                    });

                    li.appendChild(img);
                    li.appendChild(link);
                    ul.appendChild(li);
                });
            } catch (error) {
                console.error("Error al buscar usuarios:", error);
            }
        }, 600); // ⏱️ Delay de 400ms entre peticiones
    });
});
