import * as actionTypes from '../action-types';
// import Raven from 'raven-js';
import log from '../lib/logging.js';
import { CALL_API } from '../middleware/api';
import request from 'superagent';
import Cookies from 'js-cookie';
import { addMessage } from './message-actions';
import { isExceptionDetail, isListOfErrors, getErrorMessage } from '../lib/utils/response-types';

// custom API domain for local dev testing
// let { API_DOMAIN = '' } = process.env;
// For some dumb reason fetch isn't adding the domain for POST requests, when testing we need
// a full domain in order for nock to work.
// if (process.env.NODE_ENV === 'test') { API_DOMAIN = 'http://localhost:80'; }


/**
 * Get Basic User Information.
 */
export const fetchUser = () => (dispatch) => {
  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.FETCH_USER,
        actionTypes.FETCH_USER__SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: '/api/account/user/',
    },
  });

  // Return the promise chain in case we want to use it elsewhere.
  return apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      return dispatch({
        type: actionTypes.FETCH_USER__FAIL,
        response: action,
      });
    }

    return action;
  });
};


/**
 * Update user email + password.
 */
function updateUserEmailPassSuccess(body) {
  return {
    type: actionTypes.UPDATE_USER_EMAIL_PASS_SUCCESS,
    body,
  };
}

function updateUserEmailPassFail(body) {
  return {
    type: actionTypes.UPDATE_USER_EMAIL_PASS_FAIL,
    body,
  };
}

/**
 * Do some basic client-side validation - the important stuff should be done
 * on the server.
 */
function validateUserEmailPass(data) {
  const errors = {};

  if (data.password !== data.passwordConfirm) {
    errors.password = ['Passwords do not match'];
  }

  if (data.email === '') {
    errors.email = ['Email cannot be empty'];
  }

  return errors;
}

export function updateUserEmailPass(formData = {}) {
  return (dispatch) => {
    const postData = formData;
    // Check data for errors.
    const errors = validateUserEmailPass(postData);
    // if we have errors, pass them back to the component via props.
    if (Object.keys(errors).length) {
      return dispatch(updateUserEmailPassFail({ errors }));
    }

    // If no new password was entered, don't send it to the server.
    if (postData.password === '') {
      delete postData.password;
      delete postData.passwordConfirm;
    } else {
      // Set the post value to be underscore-ized because this is what the server expects.
      postData.password_confirm = postData.passwordConfirm;
      delete postData.passwordConfirm;
    }

    // If we don't have any errors, send the request to the server.
    request
    .post('/api/account/settings/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .send(postData)
    .end((err, res) => {
      if (err) {
        // We have a data validation error that contains specific error messages.
        if (res.status === 400) {
          return dispatch(updateUserEmailPassFail({ errors: res.body }));
        }
        // Catch-all for any other error responseactionTypes.
        return dispatch(updateUserEmailPassFail({ errors: { password: [res.body.detail] } }));
      }

      return dispatch(updateUserEmailPassSuccess(res.body));
    });
  };
}


/**
 * User cash balance actions.
 */
function fetchingCashBalance() {
  return {
    type: actionTypes.FETCHING_CASH_BALANCE,
  };
}


function fetchCashBalanceFail(body) {
  return {
    type: actionTypes.FETCH_CASH_BALANCE_FAIL,
    body,
  };
}


function fetchCashBalanceSuccess(body) {
  return {
    type: actionTypes.FETCH_CASH_BALANCE_SUCCESS,
    body,
  };
}


function fetchCashBalance() {
  return (dispatch) => {
    dispatch(fetchingCashBalance());

    return new Promise((resolve, reject) => {
      request
      .get('/api/cash/balance/')
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'X-CSRFToken': Cookies.get('csrftoken'),
        Accept: 'application/json',
      })
      .end((err, res) => {
        if (err) {
          log.error("Could not fetch user's cash balance", err);
          reject(err);
          dispatch(fetchCashBalanceFail());
        } else {
          dispatch(fetchCashBalanceSuccess(res.body));
          resolve(res);
        }
      });
    });
  };
}


/**
 * Get the balance on a user's account.
 */
export function fetchCashBalanceIfNeeded() {
  return (dispatch, getState) => {
    log.info('fetchCashBalanceIfNeeded()');
    const state = getState();
    // Are we already fetching it?
    if (!state.user.cashBalance.isFetching) {
      // This will return a promise.
      return dispatch(fetchCashBalance());
    }

    // Even if we don't fetch anything, we still return a resolved promise so
    // we don't break the interface.
    return Promise.resolve();
  };
}


export function fetchEmailNotificationSettings() {
  return (dispatch) => {
    dispatch({
      type: actionTypes.FETCH_EMAIL_NOTIFICATIONS,
    });

    return new Promise((resolve, reject) => {
      request
      .get('/api/account/notifications/email/')
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'X-CSRFToken': Cookies.get('csrftoken'),
        Accept: 'application/json',
      })
      .end((err, res) => {
        if (err) {
          log.error("Could not fetch user's email notification settings", err);
          // Reject the promise.
          reject(err);

          // If validation errors are provided, pass them along.
          if (res.body.detail) {
            return dispatch({
              type: actionTypes.FETCH_EMAIL_NOTIFICATIONS_FAIL,
              body: res.detail,
            });
          }

          // If no specific validation errors, just send the response body.
          return dispatch({
            type: actionTypes.FETCH_EMAIL_NOTIFICATIONS_FAIL,
            body: res.body,
          });
        }

        dispatch({
          type: actionTypes.FETCH_EMAIL_NOTIFICATIONS_SUCCESS,
          body: res.body,
        });
        return resolve(res);
      });
    });
  };
}

export function updateEmailNotificationSettings(formData) {
  return (dispatch) => {
    dispatch({
      type: actionTypes.UPDATE_EMAIL_NOTIFICATIONS,
    });

    return new Promise((resolve, reject) => {
      request
      .post('/api/account/notifications/email/')
      .send(formData)
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'X-CSRFToken': Cookies.get('csrftoken'),
        Accept: 'application/json',
      })
      .end((err, res) => {
        if (err) {
          log.error("Could not update user's email notification settings", err);

          // If validation errors are provided, pass them along.
          if (res.body.detail) {
            return dispatch({
              type: actionTypes.UPDATE_EMAIL_NOTIFICATIONS_FAIL,
              err: res.body.detail,
            });
          }

          dispatch({
            type: actionTypes.UPDATE_EMAIL_NOTIFICATIONS_FAIL,
            err: err.message,
          });
          reject(err);
        } else {
          dispatch({
            type: actionTypes.UPDATE_EMAIL_NOTIFICATIONS_SUCCESS,
            body: res.body,
          });
          resolve(res);
        }
      });
    });
  };
}


/**
 * API GET to verify the user's location based on their IP address.
 * The user will be redirect to the invalid location page if this  doesn't
 * return a 200 response. The redirection is taken care of in the API middleware
 */
export const verifyLocation = () => (dispatch) => {
  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.VERIFY_LOCATION__SEND,
        actionTypes.VERIFY_LOCATION__SUCCESS,
        actionTypes.VERIFY_LOCATION__FAIL,
      ],
      endpoint: '/api/account/verify-location/',
    },
  });

  // Return the promise chain in case we want to use it elsewhere.
  return apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      // return dispatch({
      //   type: actionTypes.NULL,
      //   response: action.error,
      // });
    }

    return action;
  });
};


export function checkUserIdentityVerificationStatus(merchantSessionID) {
  return (dispatch) => {
    console.log('checkUserIdentityVerificationStatus', merchantSessionID);
    dispatch({ type: actionTypes.CHECK_IDENTITY_STATUS__SEND });

    return new Promise((resolve, reject) => {
      request.get(`/api/account/identity-status/${merchantSessionID}/`)
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'X-CSRFToken': Cookies.get('csrftoken'),
        Accept: 'application/json',
      })
      .send()
      .end((err, res) => {
        // There was an error.
        if (err) {
          // Is the response a general error, with a detail message?
          // If it isn't, we need to show the error banner.
          if (isExceptionDetail(res) || isListOfErrors(res) || res.statusCode === 500) {
            const message = getErrorMessage(res);

            dispatch(addMessage({
              header: 'Error while attempting to verify your identity.',
              level: 'warning',
              content: message || 'Please contact support',
            }));
          }

          // Tell the state that the request failed.
          dispatch({
            type: actionTypes.CHECK_IDENTITY_STATUS__FAIL,
            response: res.body,
          });
          // This will end up being sent to Sentry.
          return reject({ err: res.body });
        }

        // if the request went ok...
        dispatch({
          type: actionTypes.CHECK_IDENTITY_STATUS__SUCCESS,
          response: res.body,
        });

        // re-fetch the user info so our store can be up-to-date.
        dispatch(fetchUser());

        // Check the response status.
        const isVerified = res.body.status === 'SUCCESS';

        // show a pass/fail banner message.
        if (isVerified) {
          // Show a success message.
          dispatch(addMessage({
            level: 'success',
            header: 'Your identity was verified.',
            ttl: 3000,
          }));
        } else {
          dispatch(addMessage({
            header: 'Unable to verify your identity.',
            level: 'warning',
            content: 'Please contact us if you beleive this is an error.',
          }));
        }

        // Resolve the promise chain.
        return resolve({ response: res });
      });
    });
  };
}


/**
 * Verify a user's identity with Gidx.
 * @param  {Object} postData The field data form the IdentityForm component.
 * @return {Promise}
 */
export function verifyIdentity(postData) {
  return (dispatch) => {
    // Dispatch the send action.
    dispatch({ type: actionTypes.VERIFY_IDENTITY__SEND });

    return new Promise((resolve, reject) => {
      request
      .post('/api/account/verify-user/')
      .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
      .send(postData)
      .end((err, res) => {
        if (err) {
          // Is the response a general error, with a detail message?
          // If it isn't, we need to show the error banner.
          if (isExceptionDetail(res) || isListOfErrors(res) || res.statusCode === 500) {
            const message = getErrorMessage(res);

            dispatch(addMessage({
              header: 'Unable to verify your identity.',
              level: 'warning',
              content: message || 'Please contact us if you beleive this is an error.',
            }));
          }

          // Tell the state it failed.
          dispatch({
            type: actionTypes.VERIFY_IDENTITY__FAIL,
            response: res.body,
          });

          // A 400 means that the identity was not able to be verified.
          // This isn't a failed reqeust, so resolve the promise.
          if (res.statusCode === 400) {
            return resolve({ response: res });
          }

          // If it's an 'err' and it wasn't a 400, it's probably an internal
          // server error or something. Kill the promise chain. This will
          // be uncaught and sent to Sentry for reporting.
          return reject({ err: res.body });
        }

        // if it was a success...
        dispatch({
          type: actionTypes.VERIFY_IDENTITY__SUCCESS,
          response: res.body,
        });

        // Show a success message.
        dispatch(addMessage({
          level: 'success',
          header: 'Your identity was verified.',
          ttl: 3000,
        }));

        // Now that we have a verified identity, re-fetch the user info
        // so our store can be up-to-date.
        dispatch(fetchUser());

        // Resolve the promise chain.
        return resolve({ response: res });
      });
    });
  };
}


/**
 * Get && fetch user's limits .
 */

function receiveUserLimitsSuccess(body) {
  return {
    type: actionTypes.RECEIVE_USER_LIMITS_SUCCESS,
    body,
  };
}

export function fetchUserLimits(body) {
  return {
    type: actionTypes.FETCH_USER_LIMITS,
    body,
  };
}

export function receiveUserLimits() {
  return dispatch => {
    dispatch({
      type: actionTypes.RECEIVE_USER_LIMITS,
    });
    return new Promise((resolve, reject) => {
      request
          .get('/api/account/user-limits/')
          .set({
            'X-REQUESTED-WITH': 'XMLHttpRequest',
            'X-CSRFToken': Cookies.get('csrftoken'),
            Accept: 'application/json',
          })
          .end((err, res) => {
            if (err) {
              log.error("Could not fetch user's limits", err);
              reject(err);
              dispatch(addMessage({
                header: 'Unable to get your limits.',
                level: 'warning',
                content: 'Check your internet connection or reload the page',
              }));
            } else {
              const resData = Object.assign({}, res);
              resData.body.selected_values = res.body.current_values;
              dispatch(receiveUserLimitsSuccess(resData.body));
              resolve(res);
            }
          });
    });
  };
}
