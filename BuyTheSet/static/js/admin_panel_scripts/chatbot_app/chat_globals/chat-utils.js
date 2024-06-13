/**
 * Creates a new debounced function that delays invoking `func` until after `delay` milliseconds have elapsed since the last time the debounced function was invoked.
 * @param {Function} func The function to be debounced 
 * @param {number} delay The number of milliseconds to delay. 
 * @returns {Function} Returns the new debounced function.
 */
export const debounce = (func, delay) => {
    let timeoutId;
    return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    }
};

/**
 * Creates a div element with the given classes.
 * @param {string} classes The classes to add to the div. 
 * @returns {HTMLElement} Returns the new div element.
 */
export const createMessageDiv = (classes) => {
    const messageDiv = document.createElement('div');
    messageDiv.className = classes;
    return messageDiv;
};

/**
 * Toggles the visibility of the given elements.
 * @param {Array<HTMLElement>} elements the elements to toggle visibility of. 
 * @param {boolean} isVisible The visibility state to set. 
 */
export const toggleVisibility = (elements, isVisible) => {
    elements.forEach(element => element.classList.toggle('d-none', !isVisible));
};