import actionTypes from '../action-types';
import merge from 'lodash/merge';


const initialState = {
  payments: [],
  isDepositing: false,
  isWithdrawing: false,
  depositFormErrors: {},
  withdrawalFormErrors: {},
  payPalClientToken: '',
  payPalNonce: null,
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

    case actionTypes.PAYPAL_CANCELLED: {
      // Checkout was cancelled by user, dump any nonce we had.
      return merge({}, state, {
        payPalNonce: null,
      });
    }


    case actionTypes.PAYPAL_AMOUNT_CHANGED: {
      // The user changed the amount, which means we need a new nonce from
      // paypal so the one we have needs to be removed.
      return merge({}, state, {
        payPalNonce: null,
      });
    }


    case actionTypes.DEPOSITING:
      return merge({}, state, {
        isDepositing: true,
      });


    case actionTypes.DEPOSIT_SUCCESS:
      return merge({}, state, {
        isDepositing: false,
        payPalNonce: null,
        depositFormErrors: {},
      });


    case actionTypes.DEPOSIT_FAIL:
      return merge({}, state, {
        isDepositing: false,
        payPalNonce: null,
        depositFormErrors: action.ex.response.body.errors,
      });


    case actionTypes.WITHDRAW_FUNDS: {
      return merge({}, state, {
        isWithdrawing: true,
      });
    }


    case actionTypes.WITHDRAW_FUNDS_SUCCESS: {
      const newState = merge({}, state, {
        isWithdrawing: false,
      });
      newState.withdrawalFormErrors = {};
      return newState;
    }


    case actionTypes.WITHDRAW_FUNDS_FAIL: {
      const newState = merge({}, state, {
        isWithdrawing: false,
      });
      newState.withdrawalFormErrors = action.body;
      return newState;
    }


    default:
      return state;
  }
};
