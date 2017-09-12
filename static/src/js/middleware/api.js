// TODO: fix our promise warnings and enable this.
/* eslint-disable promise/no-callback-in-promise */
import Raven from 'raven-js';
import { dateNow } from '../lib/utils';
import log from '../lib/logging.js';
import Cookies from 'js-cookie';
import fetch from 'isomorphic-fetch';
import { getJsonResponse } from '../lib/utils/response-types';

// custom API domain for local dev testing
const { API_DOMAIN = '' } = process.env;

// based on https://git.io/vo1Js

// Fetches an API response and normalizes the result JSON according to schema.
// This makes every API response have the same shape, regardless of how nested it was.
const callApi = (endpoint, callback) => fetch(`${API_DOMAIN}${endpoint}`, {
  method: 'GET',
  credentials: 'same-origin',
  Accept: 'application/json',
  'X-CSRFToken': Cookies.get('csrftoken'),
}).then(response => {
  // First, reject a response that isn't in the 200 range.
  if (!response.ok) {
    return getJsonResponse(response).then((json) => {
      // If the error response is for a restricted location, immediately redirect to the
      // restricted location page.
      // This is disabled because we don't want to insta-redirect. Our new
      // default strategy is to show a modal telling the user they will not
      // be able to do some action, we can move this logic somewhere else if
      // we want to redirect on a specific action.
      // if (json.detail === 'IP_CHECK_FAILED') {
      //   window.location.href = '/restricted-location/';
      //   return Promise.reject('redirecting due to location restriction.');
      // }

      // If it wasn't a location issue, log the error, and reject the promise.
      // The provided failure action will be called after this.
      log.info(`API request was not a 2xx response: ${endpoint}`, response);

      const reason = json || response;
      return Promise.reject(reason);
    });
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

  // append localhost to tests so we can use nock
  if (process.env.NODE_ENV === 'test') endpoint = `http://localhost${endpoint}`;

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
    (error) => {
      // The 'captureMessage' above will catch any http related errors, this will catch any errors
      // in our code that occur further on in the pipeline. Without this, any errors in our reducers
      // or actions or callbacks will die silently and get passed into the failure action.
      if (error instanceof Error) {
        Raven.captureException(error);
        log.error(error.stack);
      }

      // Call the failure action (probably showing a message to the user) with the supplied info.
      return next(actionWith({
        // where to pass to
        type: failureType,
        requestType,
        error: error.detail || {},

        // what to show the user
        header: 'Failed to connect to API.',
        // Added some detailed info for non-production purposes
        // TODO: remove these when we go public.
        content: 'Please refresh the page to reconnect.',
        response: error,
        level: 'warning',
        id: 'apiFailure',
      }));
    }
  );
};
