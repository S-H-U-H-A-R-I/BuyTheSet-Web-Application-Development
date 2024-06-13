'use strict';
import { initializeWebSocket, initializeFilters } from "./product-socket.js";
import { ProductCard, initializeProductCards } from "./product-card.js";
import { createProductElement } from "./product-element.js";
const productCardInstances = new WeakMap();


function handleWebSocketMessage(e) {
    const data = JSON.parse(e.data);
    if (data.update) {
        const product = data.product;
        const productElement = document.querySelector(`[data-product-id="${product.pk}"]`).closest('.card');
        if (productElement) {
            const productCard = productCardInstances.get(productElement);
            if (productCard) {
                productCard.updateProductFields(product);
            }
        }
    } else if (data.sorted_products) {
        const productContainer = document.querySelector('.row.products');
        productContainer.innerHTML = '';
        data.sorted_products.forEach((product) => {
            const productElement = createProductElement(product);
            productContainer.appendChild(productElement);
            const productCard = new ProductCard(productElement.querySelector('.card'), productCardInstances);
            productCardInstances.set(productElement.querySelector('.card'), productCard);
            productCard.updateProductFields(product);
        });
    }
}

window.onload = () => {
    initializeWebSocket(handleWebSocketMessage);
    initializeProductCards(productCardInstances);
    initializeFilters();
}
