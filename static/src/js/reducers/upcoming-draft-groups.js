const ActionTypes = require('../action-types');
import merge from 'lodash/merge';


const initialState = {
  activeDraftGroupId: null,
  draftGroupSelectionModalIsOpen: false,
  sportContestCounts: {},
  draftGroups: {},
  // BoxScores + game info, indexed by draftGroupId.
  boxScores: {
    isFetching: false,
  },
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_UPCOMING_DRAFTGROUPS_INFO_SUCCESS:
      return merge({}, state, {
        draftGroups: action.body.draftGroups,
      });


    // Insert boxscores + games into store, indexed by the draftGroupId
    case ActionTypes.FETCH_DRAFTGROUP_BOX_SCORES_SUCCESS: {
      const stateCopy = merge({}, state);
      stateCopy.boxScores.isFetching = false;
      stateCopy.boxScores[action.response.draftGroupId] = action.response.boxScores;
      return stateCopy;
    }


    case ActionTypes.FETCHING_DRAFTGROUP_BOX_SCORES: {
      const stateCopy = merge({}, state);
      stateCopy.boxScores.isFetching = true;
      return stateCopy;
    }


    case ActionTypes.FETCH_DRAFTGROUP_BOX_SCORES_FAIL:
      return merge({}, state, {
        boxScores: merge({}, state.boxscores, {
          isFetching: false,
        }),
      });


    case ActionTypes.CLOSE_DRAFT_GROUP_SELECTION_MODAL:
      return merge({}, state, {
        draftGroupSelectionModalIsOpen: false,
      });


    case ActionTypes.OPEN_DRAFT_GROUP_SELECTION_MODAL:
      return merge({}, state, {
        draftGroupSelectionModalIsOpen: true,
      });


    case ActionTypes.SET_ACTIVE_DRAFT_GROUP_ID:
      return merge({}, state, {
        activeDraftGroupId: action.draftGroupId,
      });


    default:
      return state;
  }
};
