const ActionTypes = require('../action-types')


const initialState = {
  sportContestCounts: {},
  draftGroups: []
}


module.exports = function(state = initialState, action) {

  switch (action.type) {

    case ActionTypes.FETCH_UPCOMING_DRAFTGROUPS_INFO_SUCCESS:
      return Object.assign({}, state, {
        draftGroups: action.body.draftGroups
      });


    default:
      return state;
  }
};
