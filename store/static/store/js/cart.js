const removeForms = document.querySelectorAll(".remove-form");


removeForms.forEach((form) => {
    form.addEventListener("submit", (event) => {
        const shouldRemove = confirm(
            "Are you sure you want to remove this product?"
        );


        if (!shouldRemove) {
            event.preventDefault();
        }
    });
});
