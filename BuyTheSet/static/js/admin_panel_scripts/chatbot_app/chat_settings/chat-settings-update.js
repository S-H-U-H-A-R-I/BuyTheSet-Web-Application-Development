// Purpose: Contains functions to update chat settings.
import { messageType } from "../chat_globals/chat-message-type.js";
import { elements as es } from "./chat-settings-elements.js";
import { debounce } from "../chat_globals/chat-utils.js"


export const setupSettingsUpdateListeners = (chatSocket) => {
    es.apiKeyInput.addEventListener('blur', debounce(() => updateApiKey(chatSocket), 500));
};

const updateApiKey = (chatSocket) => {
    const apiKey = es.apiKeyInput.value.trim();
    if (apiKey.length === 0) return;
    updateSettings(chatSocket, messageType.CHAT_SETTINGS, { api_key: apiKey });
};

const updateSettings = (chatSocket, type, payload) => {
    chatSocket.sendWebSocketMessage(type, payload);
};