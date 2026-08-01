import { getLocalStorage, setLocalStorage } from './utils.mjs';

export default class Wishlist {
  constructor(listSelector, emptySelector) {
    this.listElement = document.querySelector(listSelector);
    this.emptyElement = document.querySelector(emptySelector);
  }

  init() {
    this.listElement.addEventListener('click', (event) => {
      const button = event.target.closest('button[data-action]');

      if (!button) return;

      const productId = button.dataset.id;

      if (button.dataset.action === 'cart') {
        this.moveToCart(productId);
      }

      if (button.dataset.action === 'remove') {
        this.removeItem(productId);
      }
    });

    this.render();
  }

  getItems() {
    return getLocalStorage('so-wishlist') || [];
  }

  moveToCart(productId) {
    const wishlistItems = this.getItems();

    const product = wishlistItems.find(
      (item) => String(item.Id) === productId,
    );

    if (!product) return;

    const cartItems = getLocalStorage('so-cart') || [];
    cartItems.push(product);

    setLocalStorage('so-cart', cartItems);

    this.removeItem(productId);
  }

  removeItem(productId) {
    const updatedItems = this.getItems().filter(
      (item) => String(item.Id) !== productId,
    );

    setLocalStorage('so-wishlist', updatedItems);

    this.render();
  }

  render() {
    const items = this.getItems();

    this.listElement.innerHTML = items
      .map((item) => this.itemTemplate(item))
      .join('');

    this.emptyElement.hidden = items.length > 0;
  }

  itemTemplate(item) {
    const image =
      item.Images?.PrimaryMedium ||
      item.Images?.PrimarySmall ||
      item.Image ||
      '';

    const color =
      item.Colors?.[0]?.ColorName || 'Color not available';

    return `
      <li class="wishlist-card divider">
        <a
          class="wishlist-card__image"
          href="/product_pages/index.html?product=${encodeURIComponent(item.Id)}"
        >
          <img src="${image}" alt="${item.Name}" />
        </a>

        <div class="wishlist-card__details">
          <h2 class="card__name">${item.Name}</h2>

          <p>${color}</p>

          <p class="product-card__price">
            $${item.FinalPrice}
          </p>

          <div class="wishlist-card__actions">
            <button
              data-action="cart"
              data-id="${item.Id}"
            >
              Move to Cart
            </button>

            <button
              class="remove-wishlist"
              data-action="remove"
              data-id="${item.Id}"
            >
              Remove
            </button>
          </div>
        </div>
      </li>
    `;
  }
}
