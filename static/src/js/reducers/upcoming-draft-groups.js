const ActionTypes = require('../action-types')


const initialState = {
  sportContestCounts: {},
  draftGroups: [],
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


      case ActionTypes.FETCH_DRAFTGROUP_BOXSCORES_SUCCESS:
        let boxScore = {}
        boxScore[action.draftGroupId] = action.boxScores
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


    default:
      return state;
  }
};
