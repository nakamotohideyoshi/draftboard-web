import ActionTypes from '../action-types.js'
const initialState = {}


/**
 * Messages provide a channel for the app to notify the user of something.
 *
 * There are 3 types of messages: warning, info, and success. These simply correspond with pre-set
 * CSS styles that will dictate the color of the message the user sees.
 */
module.exports = function(state=initialState, action) {
  let nextState = Object.assign({}, state)

  switch (action.type) {

    case ActionTypes.ADD_MESSAGE:
      nextState[action.id] = {
        level: action.level,
        header: action.header,
        content: action.content,
        ttl: action.ttl
      }
      return nextState


    case ActionTypes.REMOVE_MESSAGE:
      delete nextState[action.id]
      return nextState


    case ActionTypes.CLEAR_MESSAGES:
      return {}


    default:
      return state
  }
}
