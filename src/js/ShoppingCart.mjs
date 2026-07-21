import { renderListWithTemplate } from "./utils.mjs";

export default class ShoppingCart {

  constructor(cartItems, selector) {
    this.cartItems = cartItems;
    this.selector = selector;
  }


  render() {
    const parentElement = document.querySelector(this.selector);

    renderListWithTemplate(
      this.cartItemTemplate,
      parentElement,
      this.cartItems
    );
  }


  cartItemTemplate(item) {
    return `<li class="cart-card divider">
      <a href="#" class="cart-card__image">
        <img
          src="${item.Images.PrimaryMedium}"
          alt="${item.Name}"
        />
      </a>

      <a href="#">
        <h2 class="card__name">${item.Name}</h2>
      </a>

      <p class="cart-card__color">
        ${item.Colors[0].ColorName}
      </p>

      <p class="cart-card__quantity">
        qty: 1
      </p>

      <p class="cart-card__price">
        $${item.FinalPrice}
      </p>
    </li>`;
  }
}