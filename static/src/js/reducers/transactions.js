import ActionTypes from '../action-types';
import { merge as _merge } from 'lodash';


const initialState = {
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
    case ActionTypes.FETCH_TRANSACTIONS_SUCCESS:
      return _merge({}, state, {
        allTransactions: action.body,
        filteredTransactions: action.body,
      });

    case ActionTypes.FILTER_TRANSACTIONS:
      // TODO: filter out transactions if startDate / endDate provided.
      // const startDate = action.filters.startDate || state.startDate
      // const endDate = action.filters.endDate || state.endDate
      const filteredTransactions = state.allTransactions;

      return _merge({}, state, {
        filteredTransactions,
        filters: {
          startDate: action.filters.startDate,
          endDate: action.filters.endDate,
        },
      });


    case ActionTypes.TRANSACTION_FOCUSED:
      // Update the currently focused transactionId.
      return _merge(
        {}, state, { focusedTransactionId: action.transactionId }
      );


    default:
      return state;
  }
};
