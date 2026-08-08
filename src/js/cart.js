import { getLocalStorage } from './utils.mjs';

function renderCartContents() {
  const cartItems = getLocalStorage('so-cart') || [];
  const htmlItems = cartItems.map((item) => cartItemTemplate(item));
  document.querySelector('.product-list').innerHTML = htmlItems.join('');

  if (cartItems.length > 0) {
    document.querySelector('.cart-footer').classList.remove('hide');
    displayCartTotal(cartItems);
  }
}

function displayCartTotal(cartItems) {
  let total = 0;

  cartItems.forEach((item) => {
    total += item.FinalPrice;
  });

  document.querySelector('.cart-total').textContent =
    `Total: $${total.toFixed(2)}`;
}

function cartItemTemplate(item) {
  return `<li class="cart-card divider">
    <a href="${import.meta.env.BASE_URL}product_pages/index.html?product=${item.Id}" class="cart-card__image">
      <img
        src="${item.Images.PrimaryMedium}"
        alt="${item.Name}">
    </a>
    <a href="${import.meta.env.BASE_URL}product_pages/index.html?product=${item.Id}">
      <h2 class="card__name">${item.Name}</h2>
    </a>
    <p class="cart-card__color">${item.Colors[0].ColorName}</p>
    <p class="cart-card__quantity">qty: 1</p>
    <p class="cart-card__price">$${item.FinalPrice}</p>
  </li>`;
}

renderCartContents();
