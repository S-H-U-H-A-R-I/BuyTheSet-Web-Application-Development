// Initializes the chat settings page
import { setupSettingsUpdateListeners } from "./chat-settings-update.js";

export const init = (chatSocket) => {
    setupSettingsUpdateListeners(chatSocket);
};