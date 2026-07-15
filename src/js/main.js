import { loadHeaderFooter } from "./utils.mjs";
import Alert from "./Alert.js";

loadHeaderFooter();


// Alerts
async function loadAlerts() {
    const response = await fetch("/json/alerts.json");
    const alerts = await response.json();

    const mainElement = document.querySelector("main");

    const alertList = new Alert(alerts, mainElement);
    alertList.render();
}

loadAlerts();