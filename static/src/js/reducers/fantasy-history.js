import ActionTypes from'../action-types.js'

const initialState = {}


module.exports = function(state=initialState, action) {
  switch (action.type) {

    case ActionTypes.FETCH_FANTASY_HISTORY_SUCCESS:
      return Object.assign({}, state, action.body.history)

    default:
      return state
  }
}
