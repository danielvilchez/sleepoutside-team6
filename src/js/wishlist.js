import Wishlist from './Wishlist.mjs';
import { loadHeaderFooter } from './utils.mjs';

loadHeaderFooter();

const wishlist = new Wishlist(
  '.wishlist-list',
  '.wishlist-empty',
);

wishlist.init();
