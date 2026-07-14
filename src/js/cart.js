import { getLocalStorage } from "./utils.mjs";
import ShoppingCart from "./ShoppingCart.mjs";


const cartItems = getLocalStorage("so-cart");


const cart = new ShoppingCart(
  cartItems,
  ".product-list"
);


cart.render();