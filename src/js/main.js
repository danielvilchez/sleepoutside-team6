import Alert from "./Alert.js";

async function loadAlerts() {
  const response = await fetch("/json/alerts.json");
  const alerts = await response.json();
  const mainElement = document.querySelector("main");
  const alertList = new Alert(alerts, mainElement);
  alertList.render();
}

loadAlerts();
