import ExternalServices from "./ExternalServices.mjs";
import ProductList from "./ProductList.mjs";
import { getParam, loadHeaderFooter } from "./utils.mjs";

loadHeaderFooter();

const category = getParam("category") || "tents";

const titleElement = document.querySelector(".products-title");

if (titleElement) {
    titleElement.textContent = `Top Products: ${category
        .replace("-", " ")
        .replace(/\b\w/g, letter => letter.toUpperCase())}`;
}

const dataSource = new ExternalServices();

const listElement = document.querySelector(".product-list");

const productList = new ProductList(
    category,
    dataSource,
    listElement
);

productList.init();