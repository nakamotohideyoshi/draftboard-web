import * as types from '../action-types';
import 'babel-core/polyfill';
import request from 'superagent';
import Cookies from 'js-cookie';
import log from '../lib/logging.js';


function fetchUserSuccess(body) {
  return {
    type: types.FETCH_USER_SUCCESS,
    body,
  };
}


function fetchUserFail(ex) {
  return {
    type: types.FETCH_USER_FAIL,
    ex,
  };
}


export function fetchUser() {
  return (dispatch) => {
    request
      .get('/account/api/account/user/')
      .set({ 'X-REQUESTED-WITH': 'XMLHttpRequest' })
      .set('Accept', 'application/json')
      .end((err, res) => {
        if (err) {
          return dispatch(fetchUserFail(err));
        }

        return dispatch(fetchUserSuccess(res.body));
      });
  };
}


function updateUserInfoSuccess(body) {
  return {
    type: types.UPDATE_USER_INFO_SUCCESS,
    body,
  };
}


function updateUserInfoFail(ex) {
  return {
    type: types.UPDATE_USER_INFO_FAIL,
    ex,
  };
}


export function updateUserInfo(postData = {}) {
  return (dispatch) => {
    request
    .post('/account/api/account/user/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .send(postData)
    .end((err, res) => {
      if (err) {
        return dispatch(updateUserInfoFail(err));
      }

      return dispatch(updateUserInfoSuccess(res.body));
    });
  };
}


function updateUserAddressSuccess(body) {
  return {
    type: types.UPDATE_USER_ADDRESS_SUCCESS,
    body,
  };
}


function updateUserAddressFail(ex) {
  return {
    type: types.UPDATE_USER_ADDRESS_FAIL,
    ex,
  };
}


export function updateUserAddress(postData = {}) {
  return (dispatch) => {
    request
      .post('/account/api/account/information/')
      .send(postData)
      .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
      .end((err, res) => {
        if (err) {
          return dispatch(updateUserAddressFail(err));
        }

        return dispatch(updateUserAddressSuccess(res.body));
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
