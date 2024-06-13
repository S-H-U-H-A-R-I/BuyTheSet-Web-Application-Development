import { getElements } from '../chat_globals/chat-dom-helpers.js';

export const elements = getElements({
    menuModalHeader: { type: 'id', value: 'menu-modal-header' },
    menuModalBody: { type: 'id', value: 'menu-modal-body' },
    menuModalFooter: { type: 'id', value: 'menu-modal-footer' },
    messageModalHeader: { type: 'id', value: 'message-modal-header' },
    messageModalBody: { type: 'id', value: 'message-modal-body' },
    messageModalFooter: { type: 'id', value: 'message-modal-footer' },
    chatMessageLink: { type: 'selectorAll', value: '.chat-message-link' },
    chatMessageDeleteBtn: { type: 'selectorAll', value: '.chat-delete-btn' },
    modalBodySystemMessage: { type: 'selector', value: '.system-message' },
});