import merge from 'lodash/merge';

const ActionTypes = require('../action-types');
const initialState = {
  lineups: {},
  draftGroupIdFilter: null,
  draftGroupsWithLineups: [],
  lineupBeingEdited: null,
  focusedLineupId: null,
  hoveredLineupId: null,
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_UPCOMING_LINEUPS_SUCCESS: {
      // Grab the first lineup in our object and set it as focused.
      let focusedLineupId;
      if (action.lineups && Object.keys(action.lineups).length > 0) {
        focusedLineupId = action.lineups[Object.keys(action.lineups)[Object.keys(action.lineups).length - 1]].id;
      }


      // Return a copy of the previous state with our new things added to it.
      return merge({}, state, {
        lineups: action.lineups || {},
        draftGroupsWithLineups: action.draftGroupsWithLineups,
        focusedLineupId,
      });
    }

    case ActionTypes.LINEUP_FOCUSED:
      return merge({}, state, {
        focusedLineupId: action.lineupId,
      });


    case ActionTypes.LINEUP_HOVERED:
      return merge({}, state, {
        hoveredLineupId: action.lineupId,
      });


    case ActionTypes.FETCH_UPCOMING_LINEUPS_FAIL:
      return state;


    case ActionTypes.EDIT_LINEUP_INIT:
      return merge({}, state, {
        lineupBeingEdited: action.lineupId,
      });


    case ActionTypes.FILTER_UPCOMING_LINEUPS_BY_DRAFTGROUP_ID:
      return merge({}, state, {
        draftGroupIdFilter: action.draftGroupId,
      });

    default:
      return state;

  }
};
