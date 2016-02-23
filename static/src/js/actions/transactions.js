import * as types from '../action-types.js';
import request from 'superagent';


export function transactionFocused(transactionId) {
  return (dispatch) => {
    dispatch({
      type: types.TRANSACTION_FOCUSED,
      transactionId,
    });
  };
}


function fetchTransactionsSuccess(body) {
  return {
    type: types.FETCH_TRANSACTIONS_SUCCESS,
    body,
  };
}


function fetchTransactionsFail(ex) {
  return {
    type: types.FETCH_TRANSACTIONS_FAIL,
    ex,
  };
}


export function fetchTransactions() {
  return (dispatch) =>
    request
      .get('/account/api/transactions/')
      .set({ 'X-REQUESTED-WITH': 'XMLHttpRequest' })
      .set('Accept', 'application/json')
      .end((err, res) => {
        if (err) {
          return dispatch(fetchTransactionsFail(err));
        }

        return dispatch(fetchTransactionsSuccess(res.body));
      }
  );
}


export function filterTransactions(isPeriod, days, startDate = null, endDate = null) {
  return {
    type: types.FILTER_TRANSACTIONS,
    filters: {
      isPeriod,
      days,
      startDate,
      endDate,
    },
  };
}
