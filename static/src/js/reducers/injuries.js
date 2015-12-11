import ActionTypes from'../action-types.js'

const initialState = {
  injuries: {}
}


module.exports = function(state=initialState, action) {
  switch (action.type) {

    case ActionTypes.FETCH_INJURIES_SUCCESS:
      return Object.assign({}, state, action.body.injuries)

    default:
      return state
  }
}
