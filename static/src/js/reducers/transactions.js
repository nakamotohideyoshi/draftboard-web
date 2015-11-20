import ActionTypes from '../action-types'


const initialState = {
  allTransactions: [],
  filteredTransactions: [],
  filters: {
    startDate: null,
    endDate: null
  }
}


module.exports = function(state = initialState, action) {

  switch (action.type) {
    case ActionTypes.FETCH_TRANSACTIONS_SUCCESS:
      return Object.assign({}, state, {
        allTransactions: action.body,
        filteredTransactions: action.body
      });

    case ActionTypes.FILTER_TRANSACTIONS:
      // TODO: filter out transactions if startDate / endDate provided.
      // const startDate = action.filters.startDate || state.startDate
      // const endDate = action.filters.endDate || state.endDate
      const filteredTransactions = state.allTransactions

      return Object.assign({}, state, {
        filteredTransactions: filteredTransactions,
        filters: {
          startDate: action.filters.startDate,
          endDate: action.filters.endDate
        }
      });

    default:
      return state;
  }
};
