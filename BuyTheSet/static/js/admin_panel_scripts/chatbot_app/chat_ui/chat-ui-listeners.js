import { elements as es } from "./chat-ui-elements.js";
import { togglePlaceHolder } from "./chat-ui-utils.js";
import { 
    handleKeyPressOnInput, 
    getUserInput, 
    isValidInput, 
    sendUserInput, 
    updateUIAfterSending 
} from "./chat-ui-handlers.js";

export const setupInputKeyPressListener = (chatSocket) => {
    es.chatInput.addEventListener('keypress', (e) => handleKeyPressOnInput(e, chatSocket));
};

export const setupSendButtonClickListener = (chatSocket) => {
    es.chatSendBtn.addEventListener('click', () => {
        const userInput = getUserInput();
        if (isValidInput(userInput)) {
            sendUserInput(chatSocket, userInput);
            updateUIAfterSending();
        }
    });
};

export const setupPlaceHolderBehaviour = () => {
    togglePlaceHolder(true);
    es.chatInput.addEventListener('blur', () => togglePlaceHolder(true));
    es.chatInput.addEventListener('focus', () => togglePlaceHolder(false));
};