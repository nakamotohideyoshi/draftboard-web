import actionTypes from '../action-types';
import merge from 'lodash/merge';

const initialState = {
  user: {
    isFetching: false,
    isIdentityVerified: false,
    identity: {},
    userLimits: [],
    currentLimits: [],
    selectedLimits: [],
    hasFetched: false,
  },
  username: window.dfs.user.username,
  identityFormInfo: {
    errors: {},
    isSending: false,
  },
  info: {
    isFetching: false,
    isIdentityVerified: false,
  },
  infoFormErrors: {},
  infoFormSaved: false,
  emailPassFormErrors: {},
  emailPassFormSaved: false,
  cashBalance: {
    isFetching: false,
    depositSum: 0,
    depositLimit: 0,
  },
  notificationSettings: {
    isFetchingEmail: false,
    isUpdatingEmail: false,
    email: [],
    emailErrors: [],
  },
  location: {
    status: 'unknown',
    isLocationVerified: false,
    isSending: false,
    hasAttemptedToVerify: false,
    message: null,
  },
};


module.exports = (state = initialState, action) => {
  switch (action.type) {
    // Fetch user (username, cash balance, identity, etc.)
    case actionTypes.FETCH_USER: {
      return merge({}, state, {
        user: {
          isFetching: true,
        },
      });
    }

    case actionTypes.FETCH_USER__FAIL: {
      return merge({}, state, {
        user: {
          isFetching: false,
          hasFetched: true,
        },
      });
    }

    case actionTypes.FETCH_USER__SUCCESS: {
      const newState = merge({}, state);
      newState.user = action.response;
      newState.user.isFetching = false;
      newState.user.hasFetched = true;
      return newState;
    }


    // Email Pass
    case actionTypes.UPDATE_USER_EMAIL_PASS_FAIL: {
      const newState = merge({}, state, {});
      newState.emailPassFormErrors = action.body.errors || {};
      return newState;
    }


    case actionTypes.UPDATE_USER_EMAIL_PASS_SUCCESS: {
      const newState = merge({}, state, { info: action.body });
      // Clear any existing errors.
      newState.emailPassFormErrors = {};
      return newState;
    }


    /**
     * User account cash balance actions.
     */
    case actionTypes.FETCHING_CASH_BALANCE:
      return merge({}, state, {
        cashBalance: {
          isFetching: true,
        },
      });


    case actionTypes.FETCH_CASH_BALANCE_SUCCESS:
      return merge({}, state, {
        cashBalance: {
          isFetching: false,
          amount: action.body.cash_balance,
          depositLimit: action.body.deposit_limit,
          depositSum: action.body.deposit_sum,
        },
      });


    case actionTypes.FETCH_CASH_BALANCE_FAIL:
      return merge({}, state, {
        cashBalance: {
          isFetching: false,
        },
      });


    case actionTypes.FETCH_EMAIL_NOTIFICATIONS:
      return merge({}, state, {
        notificationSettings: {
          isFetchingEmail: true,
        },
      });


    case actionTypes.FETCH_EMAIL_NOTIFICATIONS_SUCCESS:
      return merge({}, state, {
        notificationSettings: {
          isFetchingEmail: false,
          email: action.body,
        },
      });


    case actionTypes.FETCH_EMAIL_NOTIFICATIONS_FAIL:
      return merge({}, state, {
        notificationSettings: {
          isFetchingEmail: false,
          emailErrors: action.body,
        },
      });


    case actionTypes.UPDATE_EMAIL_NOTIFICATIONS:
      return merge({}, state, {
        notificationSettings: {
          isUpdatingEmail: true,
        },
      });


    case actionTypes.UPDATE_EMAIL_NOTIFICATIONS_SUCCESS:
      return merge({}, state, {
        notificationSettings: {
          isUpdatingEmail: false,
          email: action.body,
        },
      });


    case actionTypes.UPDATE_EMAIL_NOTIFICATIONS_FAIL:
      return merge({}, state, {
        notificationSettings: {
          isUpdatingEmail: false,
          emailErrors: [action.err],
        },
      });

    /**
     * User's limits
     */
    case actionTypes.FETCH_USER_LIMITS:
      return merge({}, state, {
        user: {
          selectedLimits: action.body,
        },
      });

    case actionTypes.RECEIVE_USER_LIMITS_SUCCESS:
      return merge({}, state, {
        user: {
          userLimits: action.body.types,
          currentLimits: action.body.current_values,
          selectedLimits: action.body.selected_values,
        },
      });

    case actionTypes.RECEIVE_USER_LIMITS:
      return merge({}, state, {
        user: {
          userLimits: [],
        },
      });

    /**
     * User Verification
     */
    case actionTypes.VERIFY_IDENTITY__SEND: {
      return merge({}, state, {
        identityForm: {
          isSending: true,
          errors: {},
        },
      });
    }


    case actionTypes.VERIFY_IDENTITY__SUCCESS: {
      return merge({}, state, {
        identityForm: {
          isSending: false,
          errors: {},
        },
      });
    }


    case actionTypes.VERIFY_IDENTITY__FAIL: {
      return merge({}, state, {
        identityForm: {
          isSending: false,
          errors: action.response,
        },
      });
    }

    /**
     * Location Verification
     */
    case actionTypes.VERIFY_LOCATION__SEND: {
      return merge({}, state, {
        location: {
          isSending: true,
          message: 'Verifying...',
        },
      });
    }

    case actionTypes.VERIFY_LOCATION__SUCCESS: {
      return merge({}, state, {
        location: {
          isSending: false,
          hasAttemptedToVerify: true,
          isLocationVerified: true,
          status: 'verified',
          message: action.error,
        },
      });
    }

    case actionTypes.VERIFY_LOCATION__FAIL: {
      return merge({}, state, {
        location: {
          isSending: false,
          hasAttemptedToVerify: true,
          isLocationVerified: false,
          status: 'failed',
          message: action.error,
        },
      });
    }


    default:
      return state;
  }
};
