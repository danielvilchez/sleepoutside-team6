import { getLocalStorage, setLocalStorage } from './utils.mjs';
import ProductData from './ProductData.mjs';

const dataSource = new ProductData('tents');

function addProductToCart(product) {
  const cartItems = getLocalStorage('so-cart') || [];
  const existingItem = cartItems.find((item) => item.Id === product.Id);

  if (existingItem) {
    existingItem.Quantity = (existingItem.Quantity || 1) + 1;
  } else {
    product.Quantity = 1;
    cartItems.push(product);
  }

  setLocalStorage('so-cart', cartItems);
}

async function addToCartHandler(e) {
  const product = await dataSource.findProductById(e.target.dataset.id);
  addProductToCart(product);
}

document
  .getElementById('addToCart')
  .addEventListener('click', addToCartHandler);
