const ActionTypes = require('../action-types');



const initialState = {
  sport: null,
  id: null,
  isFetching: false,
  allPlayers: {},
  boxScores: [],
  filters: {
    playerSearchFilter: {},
    positionFilter: {},
    teamFilter: {
      match: [],
      count: 0
    }
  }
}


// Reducer for a single draft group - used in the draft section.
module.exports = function(state = initialState, action) {
  switch (action.type) {

    case ActionTypes.FETCHING_DRAFT_GROUPS:
      return Object.assign({}, state, {
        isFetching: true
      })


    case ActionTypes.FETCH_DRAFTGROUP_SUCCESS:
      // Return a copy of the previous state with our new things added to it.
      return Object.assign({}, state, {
        sport: action.body.sport,
        allPlayers: action.body.players,
        id: action.body.id,
        start: action.body.start,
        end: action.body.end,
        isFetching: false
      });


    case ActionTypes.SET_FOCUSED_PLAYER:
      // Grab the focused player from our list of players.
      return Object.assign({}, state, {
        focusedPlayer: state.allPlayers[action.playerId]
      });


    case ActionTypes.DRAFTGROUP_FILTER_CHANGED:
      // Override any previous filters with what has been passed.
      let filters = Object.assign({}, state.filters)
      filters[action.filter.filterName] = {
        filterProperty: action.filter.filterProperty,
        match: action.filter.match,
        count: action.filter.match.length
      }

      return Object.assign({}, state, {
        filters
      });


    case ActionTypes.FETCH_DRAFTGROUP_BOXSCORES_SUCCESS:
      return Object.assign({}, state, {
        boxScores: action.boxScores
      })

    default:
      return state;
  }
};
