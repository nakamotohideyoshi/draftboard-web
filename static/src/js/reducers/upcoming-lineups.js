import merge from 'lodash/merge';

const actionTypes = require('../action-types');
const initialState = {
  hasFetchedLineups: false,
  lineups: {},
  draftGroupIdFilter: null,
  draftGroupsWithLineups: [],
  lineupBeingEdited: null,
  focusedLineupId: null,
  hoveredLineupId: null,
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case actionTypes.FETCH_UPCOMING_LINEUPS_SUCCESS: {
      // Grab the first lineup in our object and set it as focused.
      let focusedLineupId;
      if (action.response.lineups && Object.keys(action.response.lineups).length > 0) {
        focusedLineupId = action.response.lineups[
          Object.keys(action.response.lineups)[Object.keys(action.response.lineups).length - 1]
        ].id;
      }


      // Return a copy of the previous state with our new things added to it.
      return merge({}, state, {
        lineups: action.response.lineups || {},
        draftGroupsWithLineups: action.response.draftGroupsWithLineups,
        focusedLineupId,
        hasFetchedLineups: true,
      });
    }

    case actionTypes.LINEUP_FOCUSED:
      return merge({}, state, {
        focusedLineupId: action.lineupId,
      });


    case actionTypes.LINEUP_HOVERED:
      return merge({}, state, {
        hoveredLineupId: action.lineupId,
      });


    case actionTypes.FETCH_UPCOMING_LINEUPS_FAIL:
      return state;


    case actionTypes.EDIT_LINEUP_INIT:
      return merge({}, state, {
        lineupBeingEdited: action.lineupId,
        hasFetchedLineups: true,
      });


    case actionTypes.SAVE_LINEUP_EDIT:
      return merge({}, state, {
        lineups: {
          [action.lineupId]: {
            isSaving: true,
          },
        },
      });


    case actionTypes.SAVE_LINEUP_EDIT_SUCCESS:
    case actionTypes.SAVE_LINEUP_EDIT_FAIL:
      return merge({}, state, {
        lineups: {
          [action.lineupId]: {
            isSaving: false,
          },
        },
      });


    case actionTypes.FILTER_UPCOMING_LINEUPS_BY_DRAFTGROUP_ID:
      return merge({}, state, {
        draftGroupIdFilter: action.draftGroupId,
      });

    default:
      return state;

  }
};
