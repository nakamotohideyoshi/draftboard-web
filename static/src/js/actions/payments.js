import * as actionTypes from '../action-types';
import request from 'superagent';
import Cookies from 'js-cookie';
import { CALL_API } from '../middleware/api';
import { addMessage } from './message-actions.js';
import { fetchCashBalanceIfNeeded } from './user';
import log from '../lib/logging.js';
import PubSub from 'pubsub-js';


/**
 * Payment Actions
 */
export const fetchPayPalClientToken = () => (dispatch) => {
  const apiActionResponse = dispatch({
    [CALL_API]: {
      types: [
        actionTypes.FETCHING_PAYPAL_CLIENT_TOKEN,
        actionTypes.FETCH_PAYPAL_CLIENT_TOKEN_SUCCESS,
        actionTypes.ADD_MESSAGE,
      ],
      endpoint: '/api/account/vzero/client-token/',
      callback: (json) => json,
    },
  });

  apiActionResponse.then((action) => {
    // If something fails, the 3rd action is dispatched, then this.
    if (action.error) {
      dispatch({
        type: actionTypes.FETCH_PAYPAL_CLIENT_TOKEN_FAIL,
        response: action.error,
      });
    }
  });

  // Return the promise chain in case we want to use it elsewhere.
  return apiActionResponse;
};


// Get a client token if we dont' already have one.
export const fetchPayPalClientTokenIfNeeded = () => (dispatch, getState) => {
  const appState = getState();

  if (!appState.payments.payPalClientToken) {
    log.info('No paypal client token, fetching...');
    return dispatch(fetchPayPalClientToken());
  }

  log.info('Paypal client token found, not fetching.');
  return Promise.resolve();
};


function withdrawSuccess(body) {
  return {
    type: actionTypes.WITHDRAW_AMOUNT_SUCCESS,
    body,
  };
}


function withdrawFail(ex) {
  return {
    type: actionTypes.WITHDRAW_AMOUNT_FAIL,
    ex,
  };
}


export function withdraw(postData) {
  return (dispatch) => request
    .post('/account/api/account/payments/withdraw/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .send(postData)
    .end((err, res) => {
      if (err) {
        return dispatch(withdrawFail(err));
      }

      return dispatch(withdrawSuccess(res.body));
    });
}


function depositSuccess(body) {
  return {
    type: actionTypes.DEPOSIT_SUCCESS,
    body,
  };
}


function depositFail(ex) {
  return {
    type: actionTypes.DEPOSIT_FAIL,
    ex,
  };
}


/**
 * Make a Deposit.
 * @param  {string} nonce  the nonce token from paypal.
 * @param  {number|string} amount the amount of USD to deposit.
 */
export function deposit(nonce, amount) {
  return (dispatch) => {
    if (!amount) {
      log.error('No amount was set to deposit.');
      return dispatch(depositFail('No amount was set to deposit.'));
    }

    dispatch({
      type: actionTypes.DEPOSITING,
    });

    request
    .post('/api/account/vzero/deposit/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .send({
      payment_method_nonce: nonce,
      amount,
    })
    .end((err, res) => {
      if (err) {
        dispatch(addMessage({
          level: 'warning',
          header: 'Deposit Failed',
          content: res.text,
        }));

        return dispatch(depositFail(err));
      }

      dispatch(addMessage({
        level: 'success',
        header: 'Deposit was Successful.',
        content: 'Your available funds have been updated.',
      }));

      dispatch(fetchCashBalanceIfNeeded());
      PubSub.publish('account.depositSuccess');
      return dispatch(depositSuccess(res.body));
    });
  };
}
