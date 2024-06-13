'use strict';
import ChatSocket from './chat-socket.js';
import { init as initUI } from  './chat_ui/chat-ui.js';
import { init as initMenu} from './chat_menu/chat-menu.js';
import { init as initSettings} from './chat_settings/chat-settings.js';
import { init as initNavigation } from './chat_navigation/chat-navigation.js';

const initChatApp = () => {
    const chatSocket = new ChatSocket();
    chatSocket.init();
    [initUI, initMenu, initSettings, initNavigation].forEach(init => init(chatSocket));
};

initChatApp();