// Initiate chat menu and setup listeners
import { setupListeners } from "./chat-menu-listeners.js";
import { displayChatMessage } from "./chat-menu-display.js";

export const init = (chatSocket) => {
    setupListeners(chatSocket);
};

export const handleViewConversation = (data) => {
    displayChatMessage(data);
};