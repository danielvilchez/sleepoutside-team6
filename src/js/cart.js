import { getLocalStorage, setLocalStorage } from './utils.mjs';

function combineCartItems(cartItems) {
  const combinedItems = [];

  cartItems.forEach((item) => {
    const existingItem = combinedItems.find(
      (cartItem) => cartItem.Id === item.Id,
    );

    if (existingItem) {
      existingItem.Quantity += item.Quantity || 1;
    } else {
      item.Quantity = item.Quantity || 1;
      combinedItems.push(item);
    }
  });

  return combinedItems;
}

function renderCartContents() {
  const cartItems = combineCartItems(getLocalStorage('so-cart') || []);
  setLocalStorage('so-cart', cartItems);
  const htmlItems = cartItems.map((item) => cartItemTemplate(item));
  document.querySelector('.product-list').innerHTML = htmlItems.join('');
}

function cartItemTemplate(item) {
  const totalPrice = (item.FinalPrice * item.Quantity).toFixed(2);

  const newItem = `<li class="cart-card divider">
  <a href="#" class="cart-card__image">
    <img
      src="${item.Image}"
      alt="${item.Name}"
    />
  </a>
  <a href="#">
    <h2 class="card__name">${item.Name}</h2>
  </a>
  <p class="cart-card__color">${item.Colors[0].ColorName}</p>
  <p class="cart-card__quantity">qty: ${item.Quantity}</p>
  <p class="cart-card__price">$${totalPrice}</p>
</li>`;

  return newItem;
}

renderCartContents();
