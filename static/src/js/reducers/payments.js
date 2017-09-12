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
  gidx: {
    paymentForm: {
      isFetching: false,
      formEmbed: null,
    },
    withdrawForm: {
      isFetching: false,
      formEmbed: null,
      merchantSessionId: null,
    },
  },
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

    /**
     * GIDX Deposit form
     */
    case actionTypes.FETCHING_DEPOSIT_FORM: {
      return merge({}, state, {
        gidx: {
          paymentForm: {
            isFetching: true,
            formEmbed: null,
          },
        },
      });
    }

    case actionTypes.FETCH_DEPOSIT_FORM_SUCCESS: {
      return merge({}, state, {
        gidx: {
          paymentForm: {
            isFetching: false,
            formEmbed: action.response.detail.form_embed,
          },
        },
      });
    }

    case actionTypes.FETCH_DEPOSIT_FORM_FAIL: {
      return merge({}, state, {
        gidx: {
          paymentForm: {
            isFetching: false,
          },
        },
      });
    }

    /**
     * GIDX Withdraw form
     */

    case actionTypes.FETCHING_WITHDRAW_FORM: {
      return merge({}, state, {
        gidx: {
          withdrawForm: {
            isFetching: true,
            formEmbed: null,
          },
        },
      });
    }

    case actionTypes.FETCH_WITHDRAW_FORM_SUCCESS: {
      return merge({}, state, {
        gidx: {
          withdrawForm: {
            isFetching: false,
            formEmbed: action.response.detail.form_embed,
            merchantSessionId: action.response.detail.merchant_session_id,
          },
        },
      });
    }

    case actionTypes.FETCH_WITHDRAW_FORM_FAIL: {
      return merge({}, state, {
        gidx: {
          withdrawForm: {
            isFetching: false,
          },
        },
      });
    }

    default:
      return state;
  }
};
