import { handleSettingsResponse } from './chat_settings/chat-settings-response.js';
import { populateChatMessages } from './chat_ui/chat-ui-utils.js'
import { handleViewConversation } from './chat_menu/chat-menu.js'
import { messageType } from './chat_globals/chat-message-type.js';

class ChatSocket {
    constructor() {
        this.chatSocket = null;
    }

    init() {
        if (this.chatSocket && this.chatSocket.readyState !== WebSocket.CLOSED) {
            console.warn('WebSocket connection already open');
            return;
        }
        const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        this.chatSocket = new WebSocket(`${protocol}${window.location.host}/admin_panel/ws/chat/`);
        this.chatSocket.addEventListener('error', this.handleWebSocketError.bind(this));
        this.chatSocket.addEventListener('close', this.handleWebSocketClose.bind(this));
        this.chatSocket.addEventListener('message', this.handleWebSocketMessage.bind(this));
    }

    sendWebSocketMessage(type, payload) {
        if (!this.isWebSocketOpen()) {
            console.warn('WebSocket connection is not open, message not sent.');
            return;
        }
        this.chatSocket.send(JSON.stringify({ type, ...payload }));
    }

    isWebSocketOpen() {
        return this.chatSocket.readyState === WebSocket.OPEN;
    }

    handleWebSocketError(error) {
        console.error('WebSocket error:', error);
    }

    handleWebSocketClose() {
        console.log(`WebSocket connection closed at ${new Date().toLocaleTimeString()}`);
        this.chatSocket = null;
    }

    handleWebSocketMessage(e) {
        let data;
        try {
            data = JSON.parse(e.data);
            if (!data.type) throw new Error(`Invalid message format: ${e.data}`);
            this.handleMessage(data);
        } catch (error) {
            console.error('WebSocket message error:', error);
        }
    }

    handleMessage(data) {
        switch (data.type) {
            case messageType.CHAT_MESSAGE:
                populateChatMessages(data.text, 'chat-message pre-wrap');
                break;
            case messageType.CHAT_MENU:
                handleViewConversation(data.content);
                break;
            case messageType.CHAT_SETTINGS:
                handleSettingsResponse(data);
                break;
            default:
                console.error('Invalid message type:', data.type);
        }
    }
}

export default ChatSocket;

