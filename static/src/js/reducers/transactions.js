import ActionTypes from '../action-types';
import merge from 'lodash/merge';


const initialState = {
  isFetching: false,
  allTransactions: [],
  filteredTransactions: [],
  focusedTransactionId: {},
  filters: {
    startDate: null,
    endDate: null,
  },
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_TRANSACTIONS: {
      return merge({}, state, {
        isFetching: true,
      });
    }


    case ActionTypes.FETCH_TRANSACTIONS_SUCCESS: {
      const newState = merge({}, state, {});
      newState.isFetching = false;
      newState.allTransactions = action.body;
      newState.filteredTransactions = action.body;
      return newState;
    }


    case ActionTypes.FETCH_TRANSACTIONS_FAIL: {
      return merge({}, state, {
        isFetching: false,
      });
    }

    case ActionTypes.FILTER_TRANSACTIONS: {
      // TODO: filter out transactions if startDate / endDate provided.
      // const startDate = action.filters.startDate || state.startDate
      // const endDate = action.filters.endDate || state.endDate
      const filteredTransactions = state.allTransactions;

      return merge({}, state, {
        filteredTransactions,
        filters: {
          startDate: action.filters.startDate,
          endDate: action.filters.endDate,
        },
      });
    }


    case ActionTypes.TRANSACTION_FOCUSED:
      // Update the currently focused transactionId.
      return merge(
        {}, state, { focusedTransactionId: action.transactionId }
      );


    default:
      return state;
  }
};
