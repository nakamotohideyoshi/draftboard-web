const ActionTypes = require('../action-types');


module.exports = function(state = {}, action) {
  switch (action.type) {

    case ActionTypes.FETCH_UPCOMING_LINEUPS_SUCCESS:
      // Return a copy of the previous state with our new things added to it.
      return Object.assign({}, state, {
        lineups: action.body.results,
        focusedLineupId: action.body.results[0].id
      });


    case ActionTypes.FETCH_UPCOMING_LINEUPS_FAIL:
      return [...state];


    default:
      return state;

  }
};
