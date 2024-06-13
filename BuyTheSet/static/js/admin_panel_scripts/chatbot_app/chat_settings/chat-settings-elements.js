import { getElements } from '../chat_globals/chat-dom-helpers.js';

export const elements  = getElements({
    apiKeyInput: { type: 'id', value: 'api-key' },
    chatInput: { type: 'id', value: 'chat-input' },
    chatSendBtn: { type: 'id', value: 'chat-send-btn' },
})