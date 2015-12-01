const ActionTypes = require('../action-types');

const initialState = {
  lineups: {},
  draftGroupsWithLineups: [],
  focusedLineupId: null
}

module.exports = function(state = initialState, action) {
  switch (action.type) {

    case ActionTypes.FETCH_UPCOMING_LINEUPS_SUCCESS:

      // Return a copy of the previous state with our new things added to it.
      return Object.assign({}, state, {
        lineups: action.lineups,
        draftGroupsWithLineups: action.draftGroupsWithLineups,
        // Grab the first lineup in our object and set it as focused.
        focusedLineupId: action.lineups[Object.keys(action.lineups)[0]].id
      });


    case ActionTypes.LINEUP_FOCUSED:
      return Object.assign({}, state, {
        focusedLineupId: action.lineupId
      })


    case ActionTypes.FETCH_UPCOMING_LINEUPS_FAIL:
      return state;


    default:
      return state;

  }
};
