import { renderListWithTemplate } from "./utils.mjs";

function productCardTemplate(product) {
    const hasDiscount = product.FinalPrice < product.SuggestedRetailPrice;

    const discount = hasDiscount
        ? Math.round(
            ((product.SuggestedRetailPrice - product.FinalPrice) /
                product.SuggestedRetailPrice) * 100
        )
        : 0;

    return `<li class="product-card">
    <a href="/product_pages/index.html?product=${product.Id}">
      <img src="${product.Images.PrimaryMedium}" alt="Image of ${product.Name}">

      ${hasDiscount ? `<p class="discount-badge">${discount}% OFF</p>` : ""}

      <h3 class="card__brand">${product.Brand.Name}</h3>
      <h2 class="card__name">${product.NameWithoutBrand}</h2>
      <p class="product-card__price">$${product.FinalPrice}</p>
    </a>
  </li>`;
}

export default class ProductList {
    constructor(category, dataSource, listElement) {
        this.category = category;
        this.dataSource = dataSource;
        this.listElement = listElement;
    }

    async init() {
        const list = await this.dataSource.getData(this.category);
        this.renderList(list);
    }

    renderList(list) {
        renderListWithTemplate(
            productCardTemplate,
            this.listElement,
            list
        );
    }
}