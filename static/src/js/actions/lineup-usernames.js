
const request = require('superagent-promise')(require('superagent'), Promise);

import * as ActionTypes from '../action-types';


const requestLineupUsernames = (contestId) => ({
  contestId,
  type: ActionTypes.REQUEST_LINEUP_USERNAMES,
});


const receiveLineupUsernames = (contestId, response) => ({
  contestId,
  type: ActionTypes.RECEIVE_LINEUP_USERNAMES,
  lineups: response.lineups,
});


export const fetchLineupUsernames = (contestId) => (dispatch) => {
  dispatch(requestLineupUsernames(contestId));

  return request.get(
    `/api/contest/lineup-usernames/${contestId}/`
  ).set({
    'X-REQUESTED-WITH': 'XMLHttpRequest',
    Accept: 'application/json',
  }).then(
    (res) => dispatch(receiveLineupUsernames(contestId, res.body))
  );
};
