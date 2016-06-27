import Raven from 'raven-js';
import { dateNow } from '../lib/utils';
import log from '../lib/logging.js';
import Cookies from 'js-cookie';
import fetch from 'isomorphic-fetch';


// based on https://git.io/vo1Js

// Fetches an API response and normalizes the result JSON according to schema.
// This makes every API response have the same shape, regardless of how nested it was.
const callApi = (endpoint, callback) => fetch(endpoint, {
  credentials: 'same-origin',
  Accept: 'application/json',
  'X-CSRFToken': Cookies.get('csrftoken'),
}).then(response => {
  // First, reject a response that isn't in the 200 range.
  if (!response.ok) {
    log.error(`API request failed: ${endpoint}`, response);
    // Log the request error to Sentry with some info.
    Raven.captureMessage(
      `API request failed: ${endpoint}`,
      { extra: {
        status: response.status,
        statusText: response.statusText,
        url: response.url,
      },
    });

    return Promise.reject(response);
  }

  // Otherwise parse the (hopefully) json from the response body.
  return response.json().then(json => ({ json, response }));
}).then(({ json }) => {
  // If a callback was supplied, call it.
  if (callback) return callback(json);
  // Return the json payload.
  return json;
}); // Do not catch() this here. it needs to bubble up for error handling.


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

  // pass through any additional request fields you want
  const requestFields = callAPI.requestFields || {};

  next(actionWith(Object.assign(
    {},
    {
      type: requestType,
      expiresAt: dateNow() + 1000 * 60,  // be able to try again in a minute
    },
    requestFields
  )));

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
      // Added some detailed info for non-production purposes
      // TODO: remove these when we go public.
      content: `Please refresh the page to reconnect.<br /> ${error.url}<br />${error.status} ${error.statusText} `,
      level: 'warning',
      id: 'apiFailure',
    }))
  );
};
