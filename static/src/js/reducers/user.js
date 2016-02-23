import ActionTypes from '../action-types';
import { merge as _merge } from 'lodash';

const initialState = {
  user: {},
  infoFormErrors: {},
  addressFormErrors: {},
  cashBalance: {
    isFetching: false,
  },
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_USER_SUCCESS:
      return _merge({}, state, {
        user: action.body,
      });

    case ActionTypes.UPDATE_USER_INFO_SUCCESS:
      // TODO: update user with the response
      return _merge({}, state, {
        infoFormErrors: {},
      });

    case ActionTypes.UPDATE_USER_ADDRESS_SUCCESS:
      // TODO: update user with the response
      return _merge({}, state, {
        addressFormErrors: {},
      });

    case ActionTypes.UPDATE_USER_INFO_FAIL:
      return _merge({}, state, {
        infoFormErrors: action.ex.response.body.errors,
      });

    case ActionTypes.UPDATE_USER_ADDRESS_FAIL:
      return _merge({}, state, {
        addressFormErrors: action.ex.response.body.errors,
      });


    /**
     * User account cash balance actions.
     */
    case ActionTypes.FETCHING_CASH_BALANCE:
      return _merge({}, state, {
        cashBalance: {
          isFetching: true,
        },
      });


    case ActionTypes.FETCH_CASH_BALANCE_SUCCESS:
      return _merge({}, state, {
        cashBalance: {
          isFetching: false,
          amount: action.body.cash_balance,
        },
      });


    case ActionTypes.FETCH_CASH_BALANCE_FAIL:
      return _merge({}, state, {
        cashBalance: {
          isFetching: false,
        },
      });


    default:
      return state;
  }
};
