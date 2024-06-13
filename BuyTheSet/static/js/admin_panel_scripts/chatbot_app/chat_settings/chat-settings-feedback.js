// Objective: Handle the feedback message display for the chat settings.
import { elements as es } from './chat-settings-elements.js';
import { createFeedbackMessageElement, removeExistingFeedbackMessage } from './chat-settings-utils.js';

export const displayFeedbackMessage = (message, status) => {
    const isStatusError = status === 'error';
    updateInputStyles(es.apiKeyInput, isStatusError);
    removeExistingFeedbackMessage(es.apiKeyInput);
    appendFeedbackMessage(es.apiKeyInput, createFeedbackMessageElement(message, isStatusError));
    updateChatInputStatus(es.chatInput, es.chatSendBtn, isStatusError);
};

const updateInputStyles = (inputElement, isStatusError) => {
    inputElement.classList.remove('is-invalid', 'is-valid');
    inputElement.classList.add(isStatusError ? 'is-invalid' : 'is-valid');
};

const appendFeedbackMessage = (inputElement, feedbackMessageElement) => {
    inputElement.parentNode.appendChild(feedbackMessageElement);
};

const updateChatInputStatus = (chatInput, chatSendBtn, isStatusError) => {
    isStatusError ? disableChatInput(chatInput, chatSendBtn) : enableChatInput(chatInput, chatSendBtn);
};

const disableChatInput = (chatInput, chatSendBtn) => {
    chatInput.textContent = 'Update API key to send messages.';
    chatInput.contentEditable = false;
    chatInput.classList.add('error');
    chatSendBtn.disabled = true;
    chatSendBtn.classList.add('error');
};

const enableChatInput = (chatInput, chatSendBtn) => {
    chatInput.textContent = 'Type a message...';
    chatInput.contentEditable = true;
    chatInput.classList.remove('error');
    chatSendBtn.disabled = false;
    chatSendBtn.classList.remove('error');
};