import * as ActionTypes from '../action-types.js'

const initialState = {
  isFetching: false
}

/**
 * Handle state mutations for player news entries.
 */
module.exports = function(state = initialState, action) {
  switch (action.type) {

    case ActionTypes.FETCHING_PLAYER_NEWS:
      return Object.assign({}, state, {
        isFetching: true
      })


    case ActionTypes.FETCH_PLAYER_NEWS_FAIL:
      return Object.assign({}, state, {
        isFetching: false
      })


    case ActionTypes.FETCH_PLAYER_NEWS_SUCCESS:
      let newState = Object.assign({}, state, {
        isFetching: false
      })
      // Update the sport entry with the newly fetched data.
      newState[action.sport] = action.playerNews

      return newState


    default:
      return state

  }
}
