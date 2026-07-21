import { getLocalStorage } from "./utils.mjs";
import ExternalServices from "./ExternalServices.mjs";

export default class CheckoutProcess {

    constructor(key, outputSelector) {

        this.key = key;
        this.outputSelector = outputSelector;

        this.list = [];
        this.itemTotal = 0;
        this.shipping = 0;
        this.tax = 0;
        this.orderTotal = 0;

        this.externalServices = new ExternalServices();
    }


    init() {

        this.list = getLocalStorage(this.key);

        this.calculateItemSubTotal();

    }


    calculateItemSubTotal() {

        this.itemTotal = 0;

        this.list.forEach((item) => {

            this.itemTotal += item.FinalPrice;

        });


        this.displayOrderTotals();

    }


    calculateOrderTotal() {


        // Tax 6%

        this.tax = this.itemTotal * 0.06;


        // Shipping:
        // $10 primer producto
        // $2 cada producto adicional

        if (this.list.length > 0) {

            this.shipping = 10 + ((this.list.length - 1) * 2);

        }


        this.orderTotal =
            this.itemTotal +
            this.tax +
            this.shipping;


        this.displayOrderTotals();

    }

    async checkout(formData) {

        const order = {

            orderDate: new Date().toISOString(),

            fname: formData.firstName,
            lname: formData.lastName,

            street: formData.street,
            city: formData.city,
            state: formData.state,
            zip: formData.zip,

            cardNumber: formData.cardNumber,
            expiration: formData.expiration,
            securityCode: formData.securityCode,

            items: this.list.map((item) => {

                return {
                    id: item.Id,
                    quantity: 1
                };

            }),

            orderTotal: this.orderTotal

        };


        console.log(JSON.stringify(order, null, 2));


        return await this.externalServices.checkout(order);

    }



    displayOrderTotals() {

        const subtotal =
            document.querySelector(
                `${this.outputSelector} #subtotal`
            );


        const tax =
            document.querySelector(
                `${this.outputSelector} #tax`
            );


        const shipping =
            document.querySelector(
                `${this.outputSelector} #shipping`
            );


        const total =
            document.querySelector(
                `${this.outputSelector} #order-total`
            );

        if (subtotal) {
            subtotal.innerText =
                `$${this.itemTotal.toFixed(2)}`;
        }

        if (tax) {
            tax.innerText =
                `$${this.tax.toFixed(2)}`;
        }

        if (shipping) {
            shipping.innerText =
                `$${this.shipping.toFixed(2)}`;
        }

        if (total) {
            total.innerText =
                `$${this.orderTotal.toFixed(2)}`;
        }

    }

}