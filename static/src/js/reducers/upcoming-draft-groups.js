const ActionTypes = require('../action-types');
import { merge as _merge } from 'lodash';


const initialState = {
  activeDraftGroupId: null,
  draftGroupSelectionModalIsOpen: false,
  sportContestCounts: {},
  draftGroups: [],
  // BoxScores + game info, indexed by draftGroupId.
  boxScores: {
    isFetching: false,
  },
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_UPCOMING_DRAFTGROUPS_INFO_SUCCESS:
      return _merge({}, state, {
        draftGroups: action.body.draftGroups,
      });


    // Insert boxscores + games into store, indexed by the draftGroupId
    case ActionTypes.FETCH_DRAFTGROUP_BOX_SCORES_SUCCESS:
      const stateCopy = _merge({}, state);
      stateCopy.boxScores.isFetching = false;
      stateCopy.boxScores[action.draftGroupId] = action.body;
      return stateCopy;


    case ActionTypes.FETCHING_DRAFTGROUP_BOX_SCORES:
      return _merge({}, state, {
        boxScores: _merge({}, state.boxscores, {
          isFetching: true,
        }),
      });


    case ActionTypes.FETCH_DRAFTGROUP_BOX_SCORES_FAIL:
      return _merge({}, state, {
        boxScores: _merge({}, state.boxscores, {
          isFetching: false,
        }),
      });


    case ActionTypes.CLOSE_DRAFT_GROUP_SELECTION_MODAL:
      return _merge({}, state, {
        draftGroupSelectionModalIsOpen: false,
      });


    case ActionTypes.OPEN_DRAFT_GROUP_SELECTION_MODAL:
      return _merge({}, state, {
        draftGroupSelectionModalIsOpen: true,
      });


    case ActionTypes.SET_ACTIVE_DRAFT_GROUP_ID:
      return _merge({}, state, {
        activeDraftGroupId: action.draftGroupId,
      });


    default:
      return state;
  }
};
