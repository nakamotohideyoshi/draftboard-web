import * as actionTypes from '../action-types';
import request from 'superagent';
import Cookies from 'js-cookie';
import { CALL_API } from '../middleware/api';
// import { addMessage } from './message-actions.js';
// import log from '../lib/logging.js';


/**
 * Contests Pool Entry Actions
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

// TODO: make deposit amount based on UI selected choice.
export function deposit(nonce, amount = 2) {
  return (dispatch) => request
    .post('/api/account/vzero/deposit/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .send({
      payment_method_nonce: nonce,
      amount,
    })
    .end((err, res) => {
      if (err) {
        return dispatch(depositFail(err));
      }
      return dispatch(depositSuccess(res.body));
    });
}
