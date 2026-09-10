document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".alert").forEach((alert) => {
        setTimeout(() => {
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-5px)";
            alert.style.transition = "0.5s";
            setTimeout(() => alert.remove(), 500);
        }, 4500);
    });

    document.querySelectorAll("[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            if (!confirm("¿Seguro que deseas eliminar este registro?")) {
                event.preventDefault();
            }
        });
    });
});
