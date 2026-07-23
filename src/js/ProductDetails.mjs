import { getLocalStorage, setLocalStorage, alertMessage } from "./utils.mjs";

export default class ProductDetails {
    constructor(productId, dataSource) {
        this.productId = productId;
        this.product = {};
        this.dataSource = dataSource;
    }

    async init() {
        this.product = await this.dataSource.findProductById(this.productId);

        this.renderProductDetails();

        document
            .getElementById("addToCart")
            .addEventListener("click", this.addToCart.bind(this));
    }

    addToCart() {
        const cartItems = getLocalStorage("so-cart") || [];

        cartItems.push(this.product);

        setLocalStorage("so-cart", cartItems);


        // Animación del carrito
        const cartIcon = document.querySelector(".cart");

        if (cartIcon) {
            cartIcon.classList.add("cart-animation");

            setTimeout(() => {
                cartIcon.classList.remove("cart-animation");
            }, 500);
        }


        alertMessage(`${this.product.Name} added to cart!`);
    }

    renderProductDetails() {
        document.querySelector(".product-detail").innerHTML = `
            <h3>${this.product.Brand.Name}</h3>

            <h2 class="divider">${this.product.NameWithoutBrand}</h2>

            <img class="divider"
                src="${this.product.Images.PrimaryLarge}"
                alt="${this.product.Name}" />

            <p class="product-card__price">$${this.product.FinalPrice}</p>

            <p class="product__color">${this.product.Colors[0].ColorName}</p>

            <p class="product__description">
                ${this.product.DescriptionHtmlSimple}
            </p>

            <div class="product-detail__add">
                <button id="addToCart" data-id="${this.product.Id}">
                    Add to Cart
                </button>
            </div>
        `;
    }
}