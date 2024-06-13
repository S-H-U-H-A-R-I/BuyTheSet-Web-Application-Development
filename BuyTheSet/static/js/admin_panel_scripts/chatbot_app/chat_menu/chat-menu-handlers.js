// Purpose: Contains functions that handle chat menu events.
import { elements as es } from './chat-menu-elements.js'
import { messageType } from '../chat_globals/chat-message-type.js'

export const handleChatMessageLinkClick = (chatSocket, e) => {
    const chatMessageId = e.target.closest('.chat-message-id').id;
    chatSocket.sendWebSocketMessage(messageType.CHAT_MENU, { action: 'view', id: chatMessageId });
};

export const handleDeleteClick = (chatSocket, e) => {
    const chatMessageDiv = e.target.closest('.chat-message-id');
    chatSocket.sendWebSocketMessage(messageType.CHAT_MENU, { action: 'delete', id: chatMessageDiv.id });
    chatMessageDiv.remove();
};

export const updateSystemMessage = (chatSocket) => {
    const messageId = es.messageModalBody.id;
    const systemMessage = es.modalBodySystemMessage.value;
    chatSocket.sendWebSocketMessage(messageType.CHAT_MENU, { action: 'edit', id: messageId, system_message: systemMessage });
};