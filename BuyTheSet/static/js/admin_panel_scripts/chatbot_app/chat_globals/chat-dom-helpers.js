/**
 * Function to get DOM elements based on a map of element identifiers.
 * 
 * @param {Object.<string, {type: string, value: string}>} elementMap An object where each key is the name of the element and the value is an object with the 'type' and 'value' properties.
 * @returns {Object.<string, HTMLElement|NodeListOf<HTMLElement>>} An object where each key is the name of the element and the value is the corresponding DOM element or NodeList of DOM elements.
 */
export const getElements = (elementMap) => {
    const getElementById = (id) => document.getElementById(id) || console.warn(`Element with id ${id} not found`);
    const getElementByClassName = (className) => document.getElementsByClassName(className) || console.warn(`Element with class ${className} not found`);
    const getElementBySelector = (selector) => document.querySelector(selector) || console.warn(`Element with selector ${selector} not found`);
    const getElementsBySelector = (selector) => document.querySelectorAll(selector) || console.warn(`Elements with selector ${selector} not found`);

    let elements = {};
    for (let key in elementMap) {
        switch (elementMap[key].type) {
            case 'id':
                elements[key] = getElementById(elementMap[key].value);
                break;
            case 'class':
                elements[key] = getElementByClassName(elementMap[key].value);
                break;
            case 'selector':
                elements[key] = getElementBySelector(elementMap[key].value);
                break;
            case 'selectorAll':
                elements[key] = getElementsBySelector(elementMap[key].value);
                break;
            default:
                console.warn(`Element type ${elementMap[key].type} not found`);
        }
    }
    return elements;
};