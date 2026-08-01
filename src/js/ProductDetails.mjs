import { getLocalStorage, setLocalStorage } from './utils.mjs';

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
      .getElementById('addToCart')
      .addEventListener('click', this.addToCart.bind(this));

    document
      .getElementById('addToWishlist')
      .addEventListener('click', this.addToWishlist.bind(this));

    this.updateWishlistButton();
  }

  addToCart() {
    const cartItems = getLocalStorage('so-cart') || [];
    cartItems.push(this.product);
    setLocalStorage('so-cart', cartItems);
  }

  addToWishlist() {
    const wishlistItems = getLocalStorage('so-wishlist') || [];

    const alreadySaved = wishlistItems.some(
      (item) => String(item.Id) === String(this.product.Id),
    );

    if (!alreadySaved) {
      wishlistItems.push(this.product);
      setLocalStorage('so-wishlist', wishlistItems);
    }

    this.updateWishlistButton();
  }

  updateWishlistButton() {
    const wishlistItems = getLocalStorage('so-wishlist') || [];
    const button = document.getElementById('addToWishlist');

    const alreadySaved = wishlistItems.some(
      (item) => String(item.Id) === String(this.product.Id),
    );

    if (alreadySaved) {
      button.textContent = 'Added to Wish List';
      button.disabled = true;
    }
  }

  renderProductDetails() {
    document.querySelector('.product-detail').innerHTML = `
      <h3>${this.product.Brand.Name}</h3>

      <h2 class="divider">${this.product.NameWithoutBrand}</h2>

      <img
        class="divider"
        src="${this.product.Images.PrimaryLarge}"
        alt="${this.product.Name}"
      />

      <p class="product-card__price">$${this.product.FinalPrice}</p>

      <p class="product__color">
        ${this.product.Colors[0].ColorName}
      </p>

      <p class="product__description">
        ${this.product.DescriptionHtmlSimple}
      </p>

      <div class="product-detail__actions">
        <button id="addToCart" data-id="${this.product.Id}">
          Add to Cart
        </button>

        <button
          id="addToWishlist"
          class="wishlist-button"
          data-id="${this.product.Id}"
        >
          Add to Wish List
        </button>
      </div>
    `;
  }
}
