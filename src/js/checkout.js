import CheckoutProcess from "./CheckoutProcess.mjs";
import { getLocalStorage } from "./utils.mjs";


const checkout = new CheckoutProcess(
    "so-cart",
    ".order-summary"
);


checkout.init();


// Mostrar productos del carrito

const cartItems = getLocalStorage("so-cart");

const productList = document.querySelector(".product-list");


cartItems.forEach((item) => {

    const li = document.createElement("li");

    li.innerHTML = `
        <div class="cart-card divider">

            <img 
            src="${item.Images.PrimaryMedium}" 
            alt="${item.Name}"
            >

            <h2>${item.Name}</h2>

            <p>
            Price: $${item.FinalPrice}
            </p>

            <p>
            Quantity: 1
            </p>

        </div>
    `;


    productList.appendChild(li);

});


// Calcular totales después del Zip Code

const zipInput = document.querySelector(
    'input[name="zip"]'
);


if (zipInput) {

    zipInput.addEventListener("blur", () => {

        checkout.calculateOrderTotal();

    });

}



const form = document.querySelector("#checkout-form");


if (form) {

    form.addEventListener("submit", (event) => {

        event.preventDefault();

        alert("Order submitted!");

    });

}