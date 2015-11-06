const ActionTypes = require('../action-types');


module.exports = function(state = {}, action) {
  switch (action.type) {

    case ActionTypes.FETCH_DRAFTGROUP_SUCCESS:
      // Return a copy of the previous state with our new things added to it.
      return Object.assign({}, state, {
        sport: action.body.sport,
        allPlayers: action.body.players
      });


    case ActionTypes.FETCH_DRAFTGROUP_REQUEST:
      console.log('FETCH_DRAFTGROUP_REQUEST()');
      return [...state];


    default:
      return state;
  }
};
