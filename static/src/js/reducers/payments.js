import actionTypes from '../action-types';
import merge from 'lodash/merge';


const initialState = {
  payments: [],
  depositFormErrors: {},
  withdrawalFormErrors: {},
  payPalClientToken: '',
  payPalNonce: '',
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case actionTypes.FETCH_PAYPAL_CLIENT_TOKEN_SUCCESS: {
      return merge({}, state, {
        payPalClientToken: action.response.client_token,
      });
    }


    case actionTypes.PAYPAL_NONCE_RECEIVED: {
      return merge({}, state, {
        payPalNonce: action.nonce,
      });
    }


    case actionTypes.DEPOSIT_SUCCESS:
      return merge({}, state, {
        depositFormErrors: {},
      });


    case actionTypes.DEPOSIT_FAIL:
      return merge({}, state, {
        depositFormErrors: action.ex.response.body.errors,
      });


    case actionTypes.WITHDRAW_AMOUNT_SUCCESS:
      return merge({}, state, {
        withdrawalFormErrors: {},
      });


    case actionTypes.WITHDRAW_AMOUNT_FAIL:
      return merge({}, state, {
        withdrawalFormErrors: action.ex.response.body.errors,
      });


    default:
      return state;
  }
};
