// import Raven from 'raven-js';
import * as actionTypes from '../action-types';
import request from 'superagent';
import Cookies from 'js-cookie';
import { CALL_API } from '../middleware/api';
import { addMessage } from './message-actions.js';
import { fetchCashBalanceIfNeeded } from './user';
import log from '../lib/logging.js';
import PubSub from 'pubsub-js';
import * as responseTypes from '../lib/utils/response-types';


export const fetchDepositForm = () => ({
  // Fetch the GIDX deposit form.
  [CALL_API]: {
    types: [
      actionTypes.FETCHING_DEPOSIT_FORM,
      actionTypes.FETCH_DEPOSIT_FORM_SUCCESS,
      actionTypes.FETCH_DEPOSIT_FORM_FAIL,
    ],
    endpoint: '/api/account/deposit-form/',
    callback: (json) => json,
  },
});

/**
 * Payment Actions
 */
export const fetchPayPalClientToken = () => ({
  // We don't notify use of failures because we'll let a BraintreeError take care of that.
  // This will fail due to an invalid location check.
  [CALL_API]: {
    types: [
      actionTypes.FETCHING_PAYPAL_CLIENT_TOKEN,
      actionTypes.FETCH_PAYPAL_CLIENT_TOKEN_SUCCESS,
      actionTypes.FETCH_PAYPAL_CLIENT_TOKEN_FAIL,
    ],
    endpoint: '/api/account/vzero/client-token/',
    callback: (json) => json,
  },
});


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
    type: actionTypes.WITHDRAW_FUNDS_SUCCESS,
    body,
  };
}


function withdrawFail(body) {
  return {
    type: actionTypes.WITHDRAW_FUNDS_FAIL,
    body,
  };
}


export function withdraw(postData) {
  return (dispatch) => {
    dispatch({
      type: actionTypes.WITHDRAW_FUNDS,
    });

    request
    .post('/api/cash/withdraw/paypal/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .send(postData)
    .end((err, res) => {
      if (err) {
        // Placeholder to determine the message to show the user.
        let content = '';

        // It's a field validation error.
        if (responseTypes.isFieldValidationErrorObject(res)) {
          // A general APIException was thown, just show a banner message.
          if (responseTypes.isExceptionDetail(res)) {
            content = res.body.detail;
          }

          // Show error banner to user.
          dispatch(addMessage({
            level: 'warning',
            header: 'Withdraw Failed',
            content,
          }));

          return dispatch(withdrawFail(res.body));
        }

        // If it's an array, it is a vanilla request error.
        if (responseTypes.isExceptionDetail(res)) {
          content = res.body[0];
        }

        // It's a server error.
        // If there is text provided in the body, display that.
        if (responseTypes.isRawTextError(res)) {
          content = res.body;
        } else {
          // Otherwise we don't know wtf this is, probably a nasty 500 bubbling up.
          content = res.statusText;
        }

        // Show error banner to user.
        dispatch(addMessage({
          level: 'warning',
          header: 'Withdraw Failed',
          content,
        }));

        return dispatch(withdrawFail({ nonField: [res.body] }));
      }

      // Request succeeded.
      dispatch(addMessage({
        level: 'success',
        header: 'Success',
        content: 'Withdraw request submitted for approval',
      }));
      PubSub.publish('account.withdrawSuccess');
      return dispatch(withdrawSuccess(res));
    });
  };
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
