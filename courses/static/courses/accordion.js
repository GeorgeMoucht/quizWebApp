document.addEventListener("DOMContentLoaded", () => {
    const accordionHeaders = document.querySelectorAll(".accordion-header");

    accordionHeaders.forEach((header) => {
        header.addEventListener("click", () => {
            const accordionItem = header.parentElement;
            const icon = header.querySelector(".icon");

            // Κλείσε όλα τα ανοιχτά accordions
            document.querySelectorAll(".accordion-item").forEach((item) => {
                if (item !== accordionItem) {
                    item.classList.remove("active");
                    const otherIcon = item.querySelector(".icon");
                    if (otherIcon) {
                        otherIcon.textContent = "+"; // Επαναφορά σε '+'
                    }
                }
            });

            // Άνοιξε/κλείσε το επιλεγμένο accordion
            accordionItem.classList.toggle("active");
            if (icon) {
                icon.textContent = accordionItem.classList.contains("active") ? "-" : "+";
            }
        });
    });
});
