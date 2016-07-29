import ActionTypes from '../action-types';
import merge from 'lodash/merge';

const initialState = {
  username: window.dfs.user.username,
  info: {
    isFetching: false,
  },
  infoFormErrors: {},
  infoFormSaved: false,
  addressFormErrors: {},
  emailPassFormErrors: {},
  emailPassFormSaved: false,
  cashBalance: {
    isFetching: false,
  },
  notificationSettings: {
    isFetchingEmail: false,
    isUpdatingEmail: false,
    email: [],
    emailErrors: [],
  },
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    // Fetch user info (name, address, dob)
    case ActionTypes.FETCH_USER_INFO_SUCCESS: {
      const newState = merge({}, state, {
        info: action.body,
      });
      newState.infoFormErrors = {};
      return newState;
    }


    case ActionTypes.UPDATE_USER_INFO_SUCCESS: {
      // TODO: update user with the response
      const newState = merge({}, state, {
        info: action.body,
      });
      newState.infoFormErrors = {};
      return newState;
    }


    case ActionTypes.UPDATE_USER_INFO_FAIL: {
      const newState = merge({}, state, {});
      newState.infoFormErrors = action.body;
      return newState;
    }


    // Email Pass
    case ActionTypes.UPDATE_USER_EMAIL_PASS_FAIL: {
      const newState = merge({}, state, {});
      newState.emailPassFormErrors = action.body.errors || {};
      return newState;
    }


    case ActionTypes.UPDATE_USER_EMAIL_PASS_SUCCESS: {
      const newState = merge({}, state, { info: action.body });
      // Clear any existing errors.
      newState.emailPassFormErrors = {};
      return newState;
    }


    /**
     * User account cash balance actions.
     */
    case ActionTypes.FETCHING_CASH_BALANCE:
      return merge({}, state, {
        cashBalance: {
          isFetching: true,
        },
      });


    case ActionTypes.FETCH_CASH_BALANCE_SUCCESS:
      return merge({}, state, {
        cashBalance: {
          isFetching: false,
          amount: action.body.cash_balance,
        },
      });


    case ActionTypes.FETCH_CASH_BALANCE_FAIL:
      return merge({}, state, {
        cashBalance: {
          isFetching: false,
        },
      });


    case ActionTypes.FETCH_EMAIL_NOTIFICATIONS:
      return merge({}, state, {
        notificationSettings: {
          isFetchingEmail: true,
        },
      });


    case ActionTypes.FETCH_EMAIL_NOTIFICATIONS_SUCCESS:
      return merge({}, state, {
        notificationSettings: {
          isFetchingEmail: false,
          email: action.body,
        },
      });


    case ActionTypes.FETCH_EMAIL_NOTIFICATIONS_FAIL:
      return merge({}, state, {
        notificationSettings: {
          isFetchingEmail: false,
          emailErrors: action.body,
        },
      });


    case ActionTypes.UPDATE_EMAIL_NOTIFICATIONS:
      return merge({}, state, {
        notificationSettings: {
          isUpdatingEmail: true,
        },
      });


    case ActionTypes.UPDATE_EMAIL_NOTIFICATIONS_SUCCESS:
      return merge({}, state, {
        notificationSettings: {
          isUpdatingEmail: false,
          email: action.body,
        },
      });


    case ActionTypes.UPDATE_EMAIL_NOTIFICATIONS_FAIL:
      return merge({}, state, {
        notificationSettings: {
          isUpdatingEmail: false,
          emailErrors: [action.err],
        },
      });


    default:
      return state;
  }
};
