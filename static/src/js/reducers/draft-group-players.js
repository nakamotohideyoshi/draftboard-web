import { merge as _merge } from 'lodash';
import * as ActionTypes from '../action-types.js';


const initialState = {
  sport: null,
  id: null,
  isFetching: false,
  allPlayers: {},
  probablePitchers: [],
};


/**
 * Reducer for the players of a single draft group - used in the draft section.
 */
module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCHING_DRAFT_GROUPS:
      return _merge({}, state, {
        isFetching: true,
      });


    case ActionTypes.FETCH_DRAFTGROUP_SUCCESS:
      // Return a copy of the previous state with our new things added to it.
      return _merge({}, state, {
        sport: action.body.sport,
        allPlayers: action.body.players,
        id: action.body.id,
        start: action.body.start,
        end: action.body.end,
        isFetching: false,
        // An array containing the values (player.srid) of probably pitchers.
        probablePitchers: action.body.game_updates.filter((update) => update.type === 'pp').map((pp) => pp.value),
      });


    default:
      return state;
  }
};
