import * as types from '../action-types.js';


/**
 * Send a message to the user via the MessageDisplay component.
 * @param {string} header       Large header text
 * @param {string} content      smaller paragraph text
 * @param {string} level        determines the style of the alert [info, success, warning]
 * @param {int} ttl             number of milleseconds to show the alert for. If ommited, the alert
 *                              will remain until the close button is clicked.
 * @param {string} id           We need a way to reference the message in order to remove it. You
 *                              can let the action create one for you, or name it so you can do
 *                              something with it later.
 */
export function addMessage(options) {
  return {
    type: types.ADD_MESSAGE,
    header: options.header,
    content: options.content,
    level: options.level || 'info',
    ttl: options.ttl,
    // Create a probably-unique-enough ID
    id: options.id || Math.random().toString(36).substr(2, 9),
    replace: options.replace || false,
  };
}


export function removeMessage(messageId) {
  return {
    type: types.REMOVE_MESSAGE,
    id: messageId,
  };
}


export function clearMessages() {
  return {
    type: types.CLEAR_MESSAGES,
  };
}
