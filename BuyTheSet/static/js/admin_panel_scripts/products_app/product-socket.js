let wsStart = 'ws://';
if (window.location.protocol === 'https:') wsStart = 'wss://';
const productEndpoint = `${wsStart}${window.location.host}/admin_panel/ws/products/`;
const filters = document.querySelectorAll('.filter input[type="checkbox"]');
let productSocket;


export function initializeWebSocket(onMessage) {
    productSocket = new WebSocket(productEndpoint);
    productSocket.onmessage = onMessage;

    productSocket.onopen = (e) => {
        onMessage({ data: JSON.stringify({ event: 'open' }) });
    };
}

export function sendUpdateToServer(productId, field, value) {
    if (!productSocket) {
        throw new Error('WebSocket is not initialized. Call initializeWebSocket() first.');
    }
    const data = {
        id: productId,
        field: field,
        value: value,
    };
    productSocket.send(JSON.stringify(data));
}

export function initializeFilters() {
    if (!productSocket) {
        throw new Error('WebSocket is not initialized. Call initializeWebSocket() first.');
    }
    filters.forEach(filter => {
        filter.addEventListener('change', () => {
            const activeFilters = Array.from(filters)
                .filter(filter => filter.checked)
                .map(filter => filter.dataset.filter);
            productSocket.send(JSON.stringify({ sort_fields: activeFilters }));
            if (filter.checked) {
                filter.parentElement.classList.add('active');
            } else {
                filter.parentElement.classList.remove('active');
            }
        });
    });
}
