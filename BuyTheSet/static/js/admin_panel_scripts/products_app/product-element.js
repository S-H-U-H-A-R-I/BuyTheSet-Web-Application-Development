export function createProductElement(product) {
    const isArchived = product.fields.is_archived ? '' : 'checked';
    let additionalImagesHTML = '';
    if (product.fields.additional_images) {
        product.fields.additional_images.forEach((image) => {
            additionalImagesHTML += /*html*/`
                <img src="${image}" class="card-img-top img-fluid rounded" alt="${product.fields.name}">
            `;
        });
    }
    let tags = '';
    if (product.fields.tags_name) {
        product.fields.tags_name.forEach((tag) => {
            tags += /*html*/`
                <span class="editable-field badge tag">${tag}</span>
            `;
        });
    }
    const productHTML = /*html*/`
        <div class="mb-4">
            <div class="card" data-product-id="${product.pk}">
                <div class="card-header">
                    <div class="card-title-container">
                        <h5 class="editable-field card-title" name="name">${product.fields.name}</h5>
                        <div class="switch-container">
                            <div class="switch-archive">
                                <input type="checkbox" id="archive-switch-${product.pk}" name="is_archived" class="archive-switch" ${isArchived}>
                                <label for="archive-switch-${product.pk}" class="thumb-archive"></label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="mb-3 product-images-container">
                        <img src="/media/${product.fields.image}" class="card-img-top img-fluid rounded" alt="${product.fields.name}">
                        ${additionalImagesHTML}
                        <div class="add-image-placeholder">
                            <i class="bi bi-plus-circle"></i>
                        </div>
                    </div>
                    <div class="tags-container">
                        ${tags}
                    </div>
                    <p class="editable-field description" name="description">${product.fields.description}</p>
                </div>
                <div class="card-footer">
                    <div class="date-created-container">
                        <span>${product.fields.date_created}</span>
                    </div>
                    <div class="edit-btn">
                        <input type="checkbox" id="edit-button-${product.pk}" class="edit-button">
                        <label for="edit-button-${product.pk}"><i class="bi bi-pencil-square"></i></label>
                    </div>
                </div>
            </div>
        </div>
    `;
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = productHTML.trim();
    return tempDiv.firstChild;
}