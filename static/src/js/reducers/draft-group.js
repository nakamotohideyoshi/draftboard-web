const ActionTypes = require('../action-types');



const initialState = {
  sport: null,
  allPlayers: {},
  filters: {
    playerSearchFilter: {},
    positionFilter: {}
  }
}


// Reducer for a single draft group - used in the draft section.
module.exports = function(state = initialState, action) {
  switch (action.type) {

    case ActionTypes.FETCH_DRAFTGROUP_SUCCESS:
      // Return a copy of the previous state with our new things added to it.
      return Object.assign({}, state, {
        sport: action.body.sport,
        allPlayers: action.body.players
      });


    case ActionTypes.SET_FOCUSED_PLAYER:
      // Grab the focused player from our list of players.
      return Object.assign({}, state, {
        focusedPlayer: state.allPlayers[action.playerId]
      });


    case ActionTypes.DRAFTGROUP_FILTER_CHANGED:
      let newFilter = {};

      newFilter[action.filter.filterName] = {
        filterProperty: action.filter.filterProperty,
        match: action.filter.match
      }

      return Object.assign({}, state, {
        filters: Object.assign({}, state.filters, newFilter)
      });

    default:
      return state;
  }
};
