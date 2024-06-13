import { sendUpdateToServer } from './product-socket.js';

export class ProductCard {
    constructor(cardElement, productCardInstances) {
        this.cardElement = cardElement;
        this.archiveSwitch = this.querySelector('.archive-switch');
        this.editSwitch = this.querySelector('.edit-button');
        this.titleElement = this.querySelector('.card-title');
        this.textElement = this.querySelector('.description');
        this.editableFields = this.querySelectorAll('.editable-field');
        this.checkboxFields = this.querySelectorAll('.checkbox-field');
        this.productId = this.cardElement.dataset.productId;
        this.originalValue = this.archiveSwitch.checked;
        this.initEventListeners();
        productCardInstances.set(cardElement, this)
    }

    querySelector(selector) {
        return this.cardElement.querySelector(selector);
    }

    querySelectorAll(selector) {
        return this.cardElement.querySelectorAll(selector);
    }

    initEventListeners() {
        this.archiveSwitch.addEventListener('change', this.handleArchiveSwitchChange.bind(this));
        this.editSwitch.addEventListener('change', this.handleEditSwitchChange.bind(this));
        this.editableFields.forEach((field) => {
            field.addEventListener('focus', this.handleElementFocus.bind(this), true);
            field.addEventListener('blur', this.handleElementBlur.bind(this), true);
        });
        this.checkboxFields.forEach((field) => {
            field.addEventListener('change', this.handleCheckboxChange.bind(this), true);
        });
    }

    handleArchiveSwitchChange() {
        const isOnline = this.archiveSwitch.checked;
        this.editSwitch.disabled = !isOnline;
        if (isOnline) {
            this.editSwitch.checked = false;
            this.updateEditableFields(false);
        }
        sendUpdateToServer(this.productId,'is_archived', !isOnline);
    }

    handleEditSwitchChange() {
        this.updateEditableFields(this.editSwitch.checked);
    }

    handleElementFocus(e) {
        this.originalValue = e.target.textContent;
    }

    handleElementBlur(e) {
        const newValue = e.target.textContent;
        if (newValue !== this.originalValue) {
            sendUpdateToServer(this.productId, e.target.getAttribute('name'), newValue);
        }
    }

    handleCheckboxChange(e) {
        const newValue = e.target.checked;
        sendUpdateToServer(this.productId, e.target.getAttribute('name'), newValue);
    }

    updateProductFields(product) {
        const isArchived = product.fields.is_archived
        this.archiveSwitch.checked = !isArchived
        this.editSwitch.disabled = !isArchived;
        if (!isArchived) {
            this.editSwitch.checked = false;
            this.updateEditableFields(false);
        }
        this.titleElement.textContent = product.fields.name;
        this.textElement.textContent = product.fields.description;
    }

    updateEditableFields(isEditable) {
        this.editableFields.forEach((field) => {
            field.contentEditable = isEditable;
        });
    }
}

export function initializeProductCards(productCardInstances) {
    document.querySelectorAll('.card').forEach((cardElement) => {
        new ProductCard(cardElement, productCardInstances);
    });
}