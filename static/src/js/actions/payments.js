import Raven from 'raven-js';
import * as actionTypes from '../action-types';
import request from 'superagent';
import Cookies from 'js-cookie';
import { CALL_API } from '../middleware/api';
import { addMessage } from './message-actions.js';
import { fetchCashBalanceIfNeeded } from './user';
import log from '../lib/logging.js';
import PubSub from 'pubsub-js';


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


/**
 * Withdraw funds - This will fetch a gidx drop-in form that will allow the user
 * to request a funds withdrawal.
 * @param options
 */
export const fetchWithdrawForm = (options) => (dispatch) => {
  if (!options || !options.amount) {
    log.error('No Amount!');
    return;
  }

  const apiActionResponse = dispatch({
    // Fetch the GIDX deposit form.
    [CALL_API]: {
      types: [
        actionTypes.FETCHING_WITHDRAW_FORM,
        actionTypes.FETCH_WITHDRAW_FORM_SUCCESS,
        actionTypes.FETCH_WITHDRAW_FORM_FAIL,
      ],
      endpoint: `/api/cash/withdraw-form/${options.amount}/`,
      callback: (json) => json,
    },
  });

  // If there were errors, show an error banner
  return apiActionResponse.then((action) => {
    if (action.error) {
      return dispatch({
        type: actionTypes.ADD_MESSAGE,
        level: 'warning',
        header: 'Unable to initialize withdrawal',
        content: action.response.detail || '',
      });
    }

    return action;
  });
};


/**
 * When a withdraw form has completed, we need to send a message to our server to create a
 * withdraw and reduce the funds of the user.
 */
export function withdrawFormCompleted(merchantSessionId) {
  return (dispatch) => {
    request
    .post('/api/cash/withdraw-session/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .send({
      session_id: merchantSessionId,
    })
    .end((err, res) => {
      if (err) {
        Raven.captureException(err);
        log.error(err, res);
      }

      dispatch(fetchCashBalanceIfNeeded());
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


export function gidxSessionComplete(sessionId) {
  return (dispatch) => {
    log.info(`gidxSessionComplete(${sessionId})`);

    if (!sessionId) {
      log.error('No sessionId was set.');
    }

    request
    .post('/api/cash/session-complete/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .send({
      session_id: sessionId,
    })
    .end((err, res) => {
      if (err) {
        log.error(err, res);
      }

      return dispatch(fetchCashBalanceIfNeeded());
    });
  };
}
