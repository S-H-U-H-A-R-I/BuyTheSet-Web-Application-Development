// Purpose: Contains functions that display chat messages in the chat menu.
import { elements as es } from "./chat-menu-elements.js";
import { toggleVisibility } from "../chat_globals/chat-utils.js";

export const displayChatMessage = (data) => {
    updateModalContent(data);
    toggleModals(
        [es.messageModalHeader, es.messageModalBody, es.messageModalFooter], true,
        [es.menuModalHeader, es.menuModalBody, es.menuModalFooter], false
    );
};

const updateModalContent = (data) => {
    const modalTitleElement = es.messageModalHeader.querySelector('.modal-title');
    const systemMessage = es.messageModalBody.querySelector('.system-message');
    modalTitleElement.textContent = data.id.substring(0, 10);
    systemMessage.value = data.system_message;
    es.messageModalBody.id = data.id;
};

const toggleModals = (esToShow, show, estoHide, hide) => {
    toggleVisibility(esToShow, show);
    toggleVisibility(estoHide, hide);
};