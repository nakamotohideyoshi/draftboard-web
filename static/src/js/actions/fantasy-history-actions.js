import * as actionTypes from '../action-types';
import { normalize, Schema, arrayOf } from 'normalizr';
import { CALL_API } from '../middleware/api';
import get from 'lodash/get';

/**
 * The Fantasy History endpoint gives us every player's last 10 games of fantasy
 * points. We use this to plot a tiny graph for each player row on the draft
 * page.
 */

const historySchema = new Schema('history', {
  idAttribute: 'player_id',
});


export const fetchFantasyHistory = (sport) => (dispatch) => {
  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.FANTASY_HISTORY__FETCHING,
        actionTypes.FANTASY_HISTORY__FETCH_SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: `/api/sports/fp-history/${sport}/`,
      callback: (json) => {
        const normalizedResponse = normalize(
          json,
          arrayOf(historySchema)
        );

        return get(normalizedResponse, 'entities.history');
      },
    },
  });

  // Return the promise chain in case we want to use it elsewhere.
  return apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      return dispatch({
        type: actionTypes.FANTASY_HISTORY__FETCH_FAIL,
        response: action.error,
        sport,
      });
    }

    return action;
  });
};
