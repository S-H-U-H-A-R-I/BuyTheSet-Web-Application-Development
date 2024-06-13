import { elements as es } from "./chat-ui-elements.js";
import { populateChatMessages } from "./chat-ui-utils.js";
import { messageType } from "../chat_globals/chat-message-type.js";

export const handleKeyPressOnInput = (e, chatSocket) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const userInput = getUserInput();
        if (isValidInput(userInput)) {
            sendUserInput(chatSocket, userInput);
            updateUIAfterSending();
        }
    }
};

export const getUserInput = () => es.chatInput.innerText.trim();

export const isValidInput = (userInput) => es.apiKeyInput.value && userInput;

export const sendUserInput = (chatSocket, userInput) => {
    chatSocket.sendWebSocketMessage(messageType.CHAT_MESSAGE, { text: userInput });
    populateChatMessages(userInput, 'chat-message-user pre-wrap', true);
};

export const updateUIAfterSending = () => {
    es.chatInput.innerText = '';
};