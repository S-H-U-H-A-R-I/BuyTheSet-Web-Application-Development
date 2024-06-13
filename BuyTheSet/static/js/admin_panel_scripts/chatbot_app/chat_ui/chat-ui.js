import { 
    setupInputKeyPressListener, 
    setupSendButtonClickListener, 
    setupPlaceHolderBehaviour 
} from "./chat-ui-listeners.js";

export const init = (chatSocket) => {
    setupPlaceHolderBehaviour();
    setupInputKeyPressListener(chatSocket);
    setupSendButtonClickListener(chatSocket);
};