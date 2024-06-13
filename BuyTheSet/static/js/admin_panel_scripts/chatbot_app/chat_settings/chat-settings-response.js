// Purpose: Handle the response from the server after sending a request to change the chat settings.
import { displayFeedbackMessage } from './chat-settings-feedback.js';

export const handleSettingsResponse = (data) => {
    const responseHandlers = {
        error: () => displayFeedbackMessage(data.error_message, 'error'),
        success: () => displayFeedbackMessage(data.success_message, 'success')
    };
    const handler = responseHandlers[data.status];
    if (handler) handler();
};