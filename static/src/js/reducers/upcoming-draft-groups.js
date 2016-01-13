const ActionTypes = require('../action-types')


const initialState = {
  activeDraftGroupId: null,
  draftGroupSelectionModalIsOpen: false,
  sportContestCounts: {},
  draftGroups: [],
  // BoxScores + game info, indexed by draftGroupId.
  boxScores: {
    isFetching: false
  }
}


module.exports = function(state = initialState, action) {

  switch (action.type) {

    case ActionTypes.FETCH_UPCOMING_DRAFTGROUPS_INFO_SUCCESS:
      return Object.assign({}, state, {
        draftGroups: action.body.draftGroups
      });


      // Insert boxscores + games into store, indexed by the draftGroupId
      case ActionTypes.FETCH_DRAFTGROUP_BOXSCORES_SUCCESS:
        let boxScore = {}
        boxScore[action.draftGroupId] = action.body
        boxScore.isFetching = false

        return Object.assign({}, state, {
          boxScores: Object.assign({}, state.boxScores, boxScore)
        })


        case ActionTypes.FETCHING_DRAFTGROUP_BOX_SCORES:
          return Object.assign({}, state, {
            boxScores: Object.assign({}, state.boxscores, {
              isFetching: true
            })
          })


        case ActionTypes.FETCH_DRAFTGROUP_BOXSCORES_FAIL:
          return Object.assign({}, state, {
            boxScores: Object.assign({}, state.boxscores, {
              isFetching: false
            })
          })


        case ActionTypes.CLOSE_DRAFT_GROUP_SELECTION_MODAL:
          return Object.assign({}, state, {
            draftGroupSelectionModalIsOpen: false
          })


        case ActionTypes.OPEN_DRAFT_GROUP_SELECTION_MODAL:
          return Object.assign({}, state, {
            draftGroupSelectionModalIsOpen: true
          })


        case ActionTypes.SET_ACTIVE_DRAFT_GROUP_ID:
          return Object.assign({}, state, {
            activeDraftGroupId: action.draftGroupId
          })


    default:
      return state;
  }
};
