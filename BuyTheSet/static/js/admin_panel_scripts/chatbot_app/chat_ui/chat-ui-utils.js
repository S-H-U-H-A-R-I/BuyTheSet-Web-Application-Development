import { elements as es } from "./chat-ui-elements.js";
import { createMessageDiv } from "../chat_globals/chat-utils.js";

let accumulatedText = '';

export const populateChatMessages = (messageData, messageClasses, isUserInput = false) => {
    const messageDiv = getMessageDiv(messageClasses);
    updateMessageDivContent(messageDiv, messageData, isUserInput);
    appendMessageDivToChat(messageDiv);
    scrollToBottomOfChatContainer();
    highlightCodeInChatMessages();
}

const getMessageDiv = (messageClasses) => {
    const lastChild = es.chatMessagesDiv.lastChild;
    return lastChild && lastChild.className === messageClasses ? lastChild : createMessageDiv(messageClasses);
};

const updateMessageDivContent = (messageDiv, data, isUserInput) => {
    isUserInput ? appendUserInputToMessageDiv(messageDiv, data) : appendChatResponseToMessageDiv(messageDiv, data);
};

const appendUserInputToMessageDiv = (messageDiv, userInput) => {
    messageDiv.innerHTML += window.marked.parse(userInput);
};

const appendChatResponseToMessageDiv = (messageDiv, chatResponse) => {
    accumulatedText += chatResponse;
    messageDiv.innerHTML = window.marked.parse(accumulatedText);
    if (!chatResponse) accumulatedText = '';
};

const appendMessageDivToChat = (messageDiv) => {
    es.chatMessagesDiv.appendChild(messageDiv);
};

const scrollToBottomOfChatContainer = () => {
    es.chatContainer.scrollTop = es.chatContainer.scrollHeight;
};

const highlightCodeInChatMessages = () => {
    es.chatMessagesDiv.querySelectorAll('pre code').forEach(hljs.highlightElement);
};


export const togglePlaceHolder = (isBlur) => {
    if (isBlur && !es.chatInput.innerText) {
        setPlaceHolderText();
    } else if (!isBlur && es.chatInput.classList.contains('placeholder')) {
        removePlaceHolderText();
    }
};

const setPlaceHolderText = () => {
    es.chatInput.innerText = es.chatInput.getAttribute('data-placeholder');
    es.chatInput.classList.add('placeholder');
};

const removePlaceHolderText = () => {
    es.chatInput.innerText = '';
    es.chatInput.classList.remove('placeholder');
};