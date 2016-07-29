import * as types from '../action-types';

import request from 'superagent';
import Cookies from 'js-cookie';
import log from '../lib/logging.js';


function fetchUserInfoSuccess(body) {
  return {
    type: types.FETCH_USER_INFO_SUCCESS,
    body,
  };
}

function fetchUserInfoFail(ex) {
  return {
    type: types.FETCH_USER_INFO_FAIL,
    ex,
  };
}

export function fetchUserInfo() {
  return (dispatch) => {
    request
      .get('/api/account/information/')
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        Accept: 'application/json',
      })
      .end((err, res) => {
        if (err) {
          return dispatch(fetchUserInfoFail(err));
        }

        return dispatch(fetchUserInfoSuccess(res.body));
      });
  };
}


/**
 * Update user information -  address, DOB, name.
 */
function updateUserInfoSuccess(body) {
  return {
    type: types.UPDATE_USER_INFO_SUCCESS,
    body,
  };
}

function updateUserInfoFail(body) {
  return {
    type: types.UPDATE_USER_INFO_FAIL,
    body,
  };
}

export function updateUserInfo(postData = {}) {
  return (dispatch) => {
    request
    .post('/api/account/information/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .send(postData)
    .end((err, res) => {
      if (err) {
        // // If validation errors are provided, pass them along.
        if (res.body.detail) {
          return dispatch(updateUserInfoFail({ fullname: [res.body.detail] }));
        }
        // Otherwise just pass the response error.
        return dispatch(updateUserInfoFail(res.body));
      }

      return dispatch(updateUserInfoSuccess(res.body));
    });
  };
}


/**
 * Update user email + password.
 */
function updateUserEmailPassSuccess(body) {
  return {
    type: types.UPDATE_USER_EMAIL_PASS_SUCCESS,
    body,
  };
}

function updateUserEmailPassFail(body) {
  return {
    type: types.UPDATE_USER_EMAIL_PASS_FAIL,
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
        // Catch-all for any other error response types.
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
    type: types.FETCHING_CASH_BALANCE,
  };
}


function fetchCashBalanceFail(body) {
  return {
    type: types.FETCH_CASH_BALANCE_FAIL,
    body,
  };
}


function fetchCashBalanceSuccess(body) {
  return {
    type: types.FETCH_CASH_BALANCE_SUCCESS,
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
      type: types.FETCH_EMAIL_NOTIFICATIONS,
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
              type: types.FETCH_EMAIL_NOTIFICATIONS_FAIL,
              body: res.detail,
            });
          }

          // If no specific validation errors, just send the response body.
          return dispatch({
            type: types.FETCH_EMAIL_NOTIFICATIONS_FAIL,
            body: res.body,
          });
        }

        dispatch({
          type: types.FETCH_EMAIL_NOTIFICATIONS_SUCCESS,
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
      type: types.UPDATE_EMAIL_NOTIFICATIONS,
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
              type: types.UPDATE_EMAIL_NOTIFICATIONS_FAIL,
              err: res.body.detail,
            });
          }

          dispatch({
            type: types.UPDATE_EMAIL_NOTIFICATIONS_FAIL,
            err: err.message,
          });
          reject(err);
        } else {
          dispatch({
            type: types.UPDATE_EMAIL_NOTIFICATIONS_SUCCESS,
            body: res.body,
          });
          resolve(res);
        }
      });
    });
  };
}
