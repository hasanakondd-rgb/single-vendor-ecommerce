document.addEventListener("DOMContentLoaded", function () {
    const checkoutForm = document.getElementById("checkout-form");


    if (!checkoutForm) {
        return;
    }


    checkoutForm.addEventListener("submit", function (event) {
        const name = document.getElementById("id_name").value.trim();
        const phone = document.getElementById("id_phone").value.trim();
        const address = document.getElementById("id_address").value.trim();


        if (name.length < 2) {
            event.preventDefault();
            alert("Please enter a valid customer name.");
            return;
        }


        if (phone.length < 7) {
            event.preventDefault();
            alert("Please enter a valid phone number.");
            return;
        }


        if (address.length < 10) {
            event.preventDefault();
            alert("Please enter a complete delivery address.");
        }
    });
});
