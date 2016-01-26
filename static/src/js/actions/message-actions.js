import * as types from '../action-types.js'
import log from '../lib/logging'



export function addMessage(content, level) {
  return {
    type: types.ADD_MESSAGE,
    level,
    content,
    // Create a probably-unique-enough ID
    id: Math.random().toString(36).substr(2, 9)
  }
}


export function removeMessage(messageId) {
  return {
    type: types.REMOVE_MESSAGE,
    id: messageId
  }
}


export function clearMessages() {
  return {
    type: types.CLEAR_MESSAGES
  }
}
