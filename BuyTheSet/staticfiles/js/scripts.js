// function displayAlert(message, alertType) {
//     const alertContainer = document.getElementById('alert-container');
//     const alertElement = document.createElement('div');
//     alertElement.classList.add('alert', `alert-${alertType}`, 'cart-message', 'pt-2', 'pb-3');
//     alertElement.setAttribute('role', 'alert');
//     alertElement.setAttribute('data-bs-autohide', 'true');
//     alertElement.innerHTML = `
//         <p class="mb-0">${message}</p>
//         <div class="progress position-absolute bottom-0 start-0 end-0 mx-3 mb-1" style="height: 5px;">
//             <div class="progress-bar custom-bg-${alertType}" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
//         </div>
//     `;
//     alertContainer.appendChild(alertElement);

//     // Start the progress bar animation
//     const progressBar = alertElement.querySelector('.progress-bar');
//     let width = 100;
//     const animationDuration = 5000;
//     const animationInterval = 30;
//     const animationStep = (100 / animationDuration) * animationInterval;

//     const animationTimer = setInterval(() => {
//         if (width <= 0) {
//             clearInterval(animationTimer);
//             alertElement.remove();
//         } else {
//             width -= animationStep;
//             progressBar.style.width = width + '%';
//         }
//     }, animationInterval);

//     // Remove the alert when the user navigatest away from the page
//     window.addEventListener('beforeunload', () => {
//         alertElement.remove();
//     });
// }


// Mobile Menu
document.addEventListener('DOMContentLoaded', function() {
    var menuButton = document.getElementById('menuButton');
    var mobileMenu = document.getElementById('mobileMenu');
    var mobileMenuClose = document.getElementById('mobileMenuClose');
  
    menuButton.addEventListener('click', function(e) {
        e.preventDefault();
        mobileMenu.style.display = 'block';
        setTimeout(function() {
            mobileMenu.classList.add('show');
        }, 10);
        document.body.style.overflow = 'hidden';
    });
  
    mobileMenuClose.addEventListener('click', function() {
        mobileMenu.classList.remove('show');
        document.body.style.overflow = 'auto';
    });
  
    mobileMenu.addEventListener('click', function(e) {
        if (e.target === mobileMenu) {
            mobileMenu.classList.remove('show');
            document.body.style.overflow = 'auto';
        }
    });
  
    mobileMenu.addEventListener('transitionend', function() {
        if (!mobileMenu.classList.contains('show')) {
            mobileMenu.style.display = 'none';
        }
    });
});


function truncateString(str, maxLength) {
    if (str.length > maxLength) {
        return str.slice(0, maxLength) + '...';
    }
    return str;
}

// Scroll to top button


// Cart Sidebar
document.addEventListener('DOMContentLoaded', function() {
    var cartLink = document.querySelector('.cart-link');

    cartLink.addEventListener('click', function(e) {
        e.preventDefault();
        fetchCartItems();
    });
});

function fetchCartItems() {
    fetch('/cart/items/', {
        method: 'GET',
        headers: {
            'X-requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        var cartItemsContainer = document.getElementById('cartItems');
        cartItemsContainer.innerHTML = ''; // Clear existing cart items
        data.cart_items.forEach((item, index) => {
            var itemHtml = createCartItemHTML(item, index, data.cart_items.length);
            cartItemsContainer.insertAdjacentHTML('beforeend', itemHtml);
        });
        attachQuantityListeners();
        attachRemoveItemListeners();
    })
    .catch(error => {
        console.error('Error loading cart items:', error);
    });
}

function createCartItemHTML(item, index, cartItemsLength) {
    return `
        <div class="cart-item">
            <a href="/product/${item.product.id}/" class="cart-item-link">
                <img src="${item.product.image_url}" alt="${item.product.name}" class="cart-item-image">
            </a>
            <div class="cart-item-details">
                <h6 class="cart-item-name" title="${item.product.name}">${truncateString(item.product.name, 20)}</h6>
                <p class="fw-bold">R${item.product.is_sale ? item.product.sale_price : item.product.price} </p>
                <div class="quantity-input">
                    <button class="quantity-btn minus-btn" data-product-id="${item.product.id}">-</button>
                    <input type="number" class="quantity-field" value="${item.quantity}" data-product-id="${item.product.id}" max="${item.product.quantity}">
                    <button class="quantity-btn plus-btn" data-product-id="${item.product.id}">+</button>
                </div>
            </div>
            <i class="bi bi-x-circle remove-item" data-product-id="${item.product.id}"></i>
        </div>
        ${index !== cartItemsLength - 1 ? '<hr class="cart-item-separator">' : ''}
    `;
}

function attachQuantityListeners() {
    var quantityFields = document.querySelectorAll('.offcanvas .quantity-field');
    var minusButtons = document.querySelectorAll('.offcanvas .minus-btn');
    var plusButtons = document.querySelectorAll('.offcanvas .plus-btn');

    quantityFields.forEach(field => {
        field.addEventListener('input', updateQuantity);
    });
    minusButtons.forEach(btn => {
        btn.addEventListener('click', decreaseQuantity);
    });
    plusButtons.forEach(btn => {
        btn.addEventListener('click', increaseQuantity);
    });
}

function attachRemoveItemListeners() {
    var removeItemButtons = document.querySelectorAll('.remove-item');
    removeItemButtons.forEach(btn => {
        btn.addEventListener('click', removeItem);
    });
}

let updateQuantityTimeout;

function updateQuantity(e) {
    var productId = e.target.dataset.productId;
    var quantity = parseInt(e.target.value);
    if (quantity >= 1) {
        clearTimeout(updateQuantityTimeout);
        updateQuantityTimeout = setTimeout(() => {
            sendUpdateQuantityRequest(productId, quantity);
        }, 500);
    }
}

function decreaseQuantity(e) {
    var productId = e.target.dataset.productId;
    var quantityField = document.querySelector(`.quantity-field[data-product-id="${productId}"]`);
    var quantity = parseInt(quantityField.value);
    if (quantity > 1) {
        quantity--;
        quantityField.value = quantity;
        clearTimeout(updateQuantityTimeout);
        updateQuantityTimeout = setTimeout(() => {
            sendUpdateQuantityRequest(productId, quantity);
        }, 500);
    }
}

function increaseQuantity(e) {
    var productId = e.target.dataset.productId;
    var quantityField = document.querySelector(`.quantity-field[data-product-id="${productId}"]`);
    var quantity = parseInt(quantityField.value);
    var maxQuantity = quantityField.max;
    console.log(quantity, maxQuantity);
    if (quantity < maxQuantity) {
        quantity++;
        quantityField.value = quantity;
        clearTimeout(updateQuantityTimeout);
        updateQuantityTimeout = setTimeout(() => {
            sendUpdateQuantityRequest(productId, quantity);
        }, 500);
    }
}

function sendUpdateQuantityRequest(productId, quantity) {
    // Send an AJAX request to update the quantity on the server
    fetch('/cart/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Quantity updated successfully');
        } else {
            console.error('Error updating quantity:', data.error);
        }
    })
    .catch(error => {
        console.error('Error updating quantity:', error);
    });
}

function removeItem(e) {
    var productId = e.target.dataset.productId;
    sendRemoveItemRequest(productId);
}

function sendRemoveItemRequest(productId) {
    fetch('/cart/delete/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            product_id: productId,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Item removed successfully');
            fetchCartItems();
            updateCartQuantity(data.cart_quantity);
        } else {
            console.error('Error removing item:', data.error);
        }
    })
    .catch(error => {
        console.error('Error removing item:', error);
    });
}

function updateCartQuantity(quantity) {
    var cartQuantityElement = document.getElementById('cart_quantity');
    cartQuantityElement.textContent = quantity;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie!== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Reload page if it is loaded from back/forward cache
window.addEventListener('pageshow', function(event) {
    if (event.persisted || (window.performance && window.performance.getEntriesByType('navigation')[0].type === 'back_forward')) {
        location.reload();
    }
});








