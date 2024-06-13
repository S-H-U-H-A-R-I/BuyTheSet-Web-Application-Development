// Objective: Handle the event listeners for the chat menu
import { elements as es } from './chat-menu-elements.js'
import { handleChatMessageLinkClick, handleDeleteClick, updateSystemMessage } from './chat-menu-handlers.js'

export const setupListeners = (chatSocket) => {
    es.chatMessageLink.forEach(link => link.addEventListener('click', (e) => handleChatMessageLinkClick(chatSocket, e)));
    es.chatMessageDeleteBtn.forEach(btn => btn.addEventListener('click', (e) => handleDeleteClick(chatSocket, e)));
    es.modalBodySystemMessage.addEventListener('blur', () => updateSystemMessage(chatSocket));
};