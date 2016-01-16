import * as ActionTypes from '../action-types.js'

const initialState = {
  isFetching: false
}

/**
 * Handle state mutations for player boxscore histories.
 *
 * These actions live in - player-history-actions.js
 */
module.exports = function(state = initialState, action) {
  switch (action.type) {

    case ActionTypes.FETCHING_PLAYER_BOX_SCORE_HISTORY:
      return Object.assign({}, state, {
        isFetching: true
      })


    case ActionTypes.FETCH_PLAYER_BOX_SCORE_HISTORY_FAIL:
      return Object.assign({}, state, {
        isFetching: false
      })


    case ActionTypes.FETCH_PLAYER_BOX_SCORE_HISTORY_SUCCESS:
      let newState = Object.assign({}, state, {
        isFetching: false
      })
      // Update the sport entry with the newly fetched data.
      newState[action.sport] = action.playerHistory

      return newState


    default:
      return state

  }
}
