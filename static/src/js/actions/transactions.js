import * as types from '../action-types.js'
import request from 'superagent'


function fetchTransactionsSuccess(body) {
  return {
    type: types.FETCH_TRANSACTIONS_SUCCESS,
    body
  };
}


function fetchTransactionsFail(ex) {
  return {
    type: types.FETCH_TRANSACTIONS_FAIL,
    ex
  };
}


export function fetchTransactions() {
  return (dispatch) => {
    return request
      .get('/account/api/transactions/')
      .set({'X-REQUESTED-WITH': 'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if (err) {
          return dispatch(fetchTransactionsFail(err))
        } else {
          return dispatch(fetchTransactionsSuccess(res.body))
        }
      });
  };
}


export function filterTransactions(startDate=null, endDate=null) {
  return {
    type: types.FILTER_TRANSACTIONS,
    filters: {
      startDate,
      endDate
    }
  };
}
