import { getElements } from '../chat_globals/chat-dom-helpers.js';

export const elements = getElements({
    chatContainer: { type: 'id', value: 'chat-container' },
    chatInput: { type: 'id', value: 'chat-input' },
    chatSendBtn: { type: 'id', value: 'chat-send-btn' },
    chatMessagesDiv: { type: 'id', value: 'chat-messages' },
    apiKeyInput: { type: 'id', value: 'api-key' },
});