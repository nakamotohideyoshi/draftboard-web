// so we can use Promises
import 'babel-core/polyfill';
const request = require('superagent-promise')(require('superagent'), Promise);
import * as ActionTypes from '../action-types';
import log from '../lib/logging';


// function requestPrize(id) {
//   log.trace('actionsLivePrize.requestPrize')
//
//   return {
//     id: id,
//     type: ActionTypes.REQUEST_PRIZE
//   }
// }


function receivePrize(id, response) {
  log.trace('actionsLivePrize.receivePrize');

  return {
    type: ActionTypes.RECEIVE_PRIZE,
    id,
    info: response,
    expiresAt: Date.now() + 86400000,
  };
}


function fetchPrize(id) {
  log.trace('actionsLivePrize.fetchPrize');

  return dispatch => {
    request.get(
      `/api/prize/${id}/`
    ).set({
      'X-REQUESTED-WITH': 'XMLHttpRequest',
      Accept: 'application/json',
    }).then((res) => {
      dispatch(receivePrize(id, res.body));
    });
  };
}


function shouldFetchPrize(state, id) {
  log.trace('actionsLivePrize.shouldFetchPrize');

  return id in state.prizes === false;
}


export function fetchPrizeIfNeeded(id) {
  log.trace('actionsLivePrize.fetchPrizeIfNeeded');

  return (dispatch, getState) => {
    if (shouldFetchPrize(getState(), id)) {
      return dispatch(fetchPrize(id));
    }

    return Promise.resolve('Prize already exists');
  };
}
