import ActionTypes from '../action-types';
import { merge as _merge } from 'lodash';


const initialState = {
  payments: [],
  depositFormErrors: {},
  withdrawalFormErrors: {},
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_PAYMENTS_SUCCESS:
      return _merge({}, state, {
        payments: action.body,
      });

    case ActionTypes.ADD_PAYMENT_METHOD_SUCCESS:
      return _merge({}, state, {
        payments: state.payments.append(action.body),
      });

    case ActionTypes.SET_PAYMENT_METHOD_DEFAULT_SUCCESS:
      return _merge({}, state, {
        payments: state.payments.map((payment) => {
          const toUpdate = payment;
          if (payment.id === action.id) {
            toUpdate.isDefault = true;
          } else {
            toUpdate.isDefault = false;
          }
          return toUpdate;
        }),
      });

    case ActionTypes.REMOVE_PAYMENT_METHOD_SUCCESS:
      return _merge({}, state, {
        payments: state.payments.filter((payment) => payment.id !== action.id),
      });

    case ActionTypes.DEPOSIT_SUCCESS:
      return _merge({}, state, {
        depositFormErrors: {},
      });

    case ActionTypes.DEPOSIT_FAIL:
      return _merge({}, state, {
        depositFormErrors: action.ex.response.body.errors,
      });

    case ActionTypes.WITHDRAW_SUCCESS:
      return _merge({}, state, {
        withdrawalFormErrors: {},
      });

    case ActionTypes.WITHDRAW_FAIL:
      return _merge({}, state, {
        withdrawalFormErrors: action.ex.response.body.errors,
      });

    default:
      return state;
  }
};
