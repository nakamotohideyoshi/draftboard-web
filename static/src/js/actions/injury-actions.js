// import request from 'superagent';
import { normalize, Schema, arrayOf } from 'normalizr';
// import log from '../lib/logging';
import actionTypes from '../action-types.js';
import { CALL_API } from '../middleware/api';


const injurySchema = new Schema('injuries', {
  idAttribute: 'player_id',
});


export const fetchSportInjuries = (sport) => (dispatch) => {
  if (!sport) {
    throw new Error('<sport> must be supplied to fetch injuries.');
  }

  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.FETCHING_INJURIES,
        actionTypes.FETCH_INJURIES_SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: `/api/sports/injuries/${sport}/`,
      callback: (json) => {
        // Normalize injuries
        const normalizedInjuries = normalize(
          json,
          arrayOf(injurySchema)
        );

        return {
          injuries: normalizedInjuries.entities.injuries,
          sport,
        };
      },
    },
  });

  apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      dispatch({
        type: actionTypes.FETCH_INJURIES_FAIL,
        response: action.error,
      });
    }
  });

  // Return the promise chain in case we want to use it elsewhere.
  return apiActionResponse;
};
