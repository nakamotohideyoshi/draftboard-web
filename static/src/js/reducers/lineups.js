const ActionTypes = require('../action-types');

const initialState = {
  lineups: {},
  draftGroupsWithLineups: [],
  focusedLineupId: null,
  hoveredLineupId: null
}

module.exports = function(state = initialState, action) {
  switch (action.type) {

    case ActionTypes.FETCH_UPCOMING_LINEUPS_SUCCESS:
      // Grab the first lineup in our object and set it as focused.
      let focusedLineupId
      if (action.lineups && action.lineups.length > 0) {
        focusedLineupId = action.lineups[Object.keys(action.lineups)[0]].id
      }

      // Return a copy of the previous state with our new things added to it.
      return Object.assign({}, state, {
        lineups: action.lineups || {},
        draftGroupsWithLineups: action.draftGroupsWithLineups,
        focusedLineupId
      });


    case ActionTypes.LINEUP_FOCUSED:
      return Object.assign({}, state, {
        focusedLineupId: action.lineupId
      })


    case ActionTypes.LINEUP_HOVERED:
      return Object.assign({}, state, {
        hoveredLineupId: action.lineupId
      })


    case ActionTypes.FETCH_UPCOMING_LINEUPS_FAIL:
      return state;


    default:
      return state;

  }
};
