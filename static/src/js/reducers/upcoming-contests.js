const ActionTypes = require('../action-types');


module.exports = function(state = {}, action) {
  switch (action.type) {

    case ActionTypes.FETCH_UPCOMING_CONTESTS_SUCCESS:
      // Return a copy of the previous state with our new things added to it.
      return Object.assign({}, state, {
        sport: action.body.sport,
        allPlayers: action.body.players
      });


    default:
      return state;
  }
};
