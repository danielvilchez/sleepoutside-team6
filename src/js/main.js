import { loadHeaderFooter } from "./utils.mjs";
import ProductData from "./ProductData.mjs";
import ProductList from "./ProductList.mjs";
import Alert from "./Alert.js";

loadHeaderFooter();


const dataSource = new ProductData("tents");

const listElement = document.querySelector(".product-list");

const productList = new ProductList(
    "tents",
    dataSource,
    listElement
);

productList.init();


// Alerts
async function loadAlerts() {
    const response = await fetch("/json/alerts.json");
    const alerts = await response.json();

    const mainElement = document.querySelector("main");

    const alertList = new Alert(alerts, mainElement);
    alertList.render();
}

loadAlerts();