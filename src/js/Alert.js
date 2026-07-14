export default class Alert {
    constructor(alerts, parent) {
        this.alerts = alerts;
        this.parent = parent;
    }

    render() {
        if (!this.alerts.length) {
            return;
        }

        const section = document.createElement("section");
        section.className = "alert-list";

        this.alerts.forEach((alert) => {
            const p = document.createElement("p");

            p.textContent = alert.message;
            p.style.backgroundColor = alert.background;
            p.style.color = alert.color;

            section.appendChild(p);
        });

        this.parent.prepend(section);
    }
}