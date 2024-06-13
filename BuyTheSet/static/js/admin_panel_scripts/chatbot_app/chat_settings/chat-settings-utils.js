/**
 * Creates a feedback message element.
 * 
 * @param {string} message The message to display. 
 * @param {boolean} isStatusError If true, the feedback is an error (invalid-feedback), otherwise it is a success message (valid-feedback)
 * @returns {HTMLElement} The created feedback message element.
 */
export const createFeedbackMessageElement = (message, isStatusError) => {
    const feedbackType = isStatusError ? 'invalid-feedback' : 'valid-feedback';
    const feedbackMessage = document.createElement('div');
    feedbackMessage.classList.add(feedbackType);
    feedbackMessage.textContent = message;
    return feedbackMessage;
};

/**
 * Removes any existing feedback message from the parent of the given input element.
 * 
 * @param {HTMLElement} inputElement The input element whose parent will be searched for a feedback message. 
 */
export const removeExistingFeedbackMessage = (inputElement) => {
    const existingFeedbackMessage = inputElement.parentNode.querySelector('.invalid-feedback, .valid-feedback');
    if (existingFeedbackMessage) existingFeedbackMessage.remove();  
};