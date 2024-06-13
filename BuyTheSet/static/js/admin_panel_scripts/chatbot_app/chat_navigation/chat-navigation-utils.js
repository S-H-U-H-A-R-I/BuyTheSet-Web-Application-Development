import { toggleVisibility } from "../chat_globals/chat-utils.js";

/**
 * Sets up a toggle button to show and hide elements when clicked.
 * 
 * @param {HTMLElement} button The button that will trigger the toggle. 
 * @param {HTMLElement[]} showElements The elements to show when the button is clicked. 
 * @param {HTMLElement[]} hideElements The elements to hide when the button is clicked. 
 */
export const setupToggleButton = (button, showElements, hideElements) => {
    button.addEventListener('click', () => {
        toggleVisibility(showElements, true);
        toggleVisibility(hideElements, false);
    });
};