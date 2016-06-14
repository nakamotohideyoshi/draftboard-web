import { dateNow } from '../lib/utils';
import fetch from 'isomorphic-fetch';


// Fetches an API response and normalizes the result JSON according to schema.
// This makes every API response have the same shape, regardless of how nested it was.
const callApi = (endpoint, callback) =>
  fetch(endpoint, {
    credentials: 'same-origin',
  }).then(response =>
    response.json().then(json => ({ json, response }))
  ).then(({ json, response }) => {
    if (!response.ok) {
      return Promise.reject(json);
    }

    if (callback) return callback(json);
    return json;
  });

// Action key that carries API call info interpreted by this Redux middleware.
export const CALL_API = Symbol('Call API');

// A Redux middleware that interprets actions with CALL_API info specified.
// Performs the call and promises when such actions are dispatched.
export default store => next => action => {
  const callAPI = action[CALL_API];
  if (typeof callAPI === 'undefined') {
    return next(action);
  }

  let { endpoint } = callAPI;
  const { types, expiresAt, callback } = callAPI;

  if (typeof endpoint === 'function') {
    endpoint = endpoint(store.getState());
  }

  if (typeof endpoint !== 'string') {
    throw new Error('Specify a string endpoint URL.');
  }
  if (!Array.isArray(types) || types.length !== 3) {
    throw new Error('Expected an array of three action types.');
  }
  if (!types.every(type => typeof type === 'string')) {
    throw new Error('Expected action types to be strings.');
  }

  function actionWith(data) {
    const finalAction = Object.assign({}, action, data);
    delete finalAction[CALL_API];
    return finalAction;
  }

  const [requestType, successType, failureType] = types;
  next(actionWith({
    type: requestType,
    expiresAt: dateNow() + 1000 * 60,  // be able to try again in a minute
  }));

  return callApi(endpoint, callback).then(
    response => next(actionWith({
      expiresAt,
      response,
      type: successType,
    })),
    error => next(actionWith({
      // where to pass to
      type: failureType,
      requestType,
      error,

      // what to show the user
      header: 'Failed to connect to API.',
      content: 'Please refresh the page to reconnect.',
      level: 'warning',
    }))
  );
};
