import { elements as es } from "./chat-navigation-elements.js";
import { setupToggleButton } from './chat-navigation-utils.js';

export const setupAppToggleButtons = () => {
    const toggles = [
        [es.menuBtn, [es.menuModalHeader, es.menuModalBody, es.menuModalFooter], [es.modalHeader, es.modalBody, es.modalFooter, es.settingsModalHeader, es.settingsModalBody, es.settingsModalFooter, es.messageModalHeader, es.messageModalBody, es.messageModalFooter]],
        [es.menuBackBtn, [es.modalHeader, es.modalBody, es.modalFooter], [es.menuModalHeader, es.menuModalBody, es.menuModalFooter]],
        [es.settingsBtn, [es.settingsModalHeader, es.settingsModalBody, es.settingsModalFooter], [es.modalHeader, es.modalBody, es.modalFooter, es.menuModalHeader, es.menuModalBody, es.menuModalFooter, es.messageModalHeader, es.messageModalBody, es.messageModalFooter]],
        [es.settingsBackBtn, [es.menuModalHeader, es.menuModalBody, es.menuModalFooter], [es.settingsModalHeader, es.settingsModalBody, es.settingsModalFooter]],
        [es.menuMessageBackBtn, [es.menuModalHeader, es.menuModalBody, es.menuModalFooter], [es.messageModalHeader, es.messageModalBody, es.messageModalFooter]]
    ];
    toggles.forEach(([button, showElements, hideElements]) => setupToggleButton(button, showElements, hideElements));
};