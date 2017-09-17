import * as types from '../action-types.js';
import request from 'superagent';
import { addMessage } from './message-actions';


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


export function fetchTransactions(startDate = null, endDate = null) {
  return (dispatch) => {
    // The server is expecting a UTC timestamp - that is the number of seconds since 1970-whatever.
    // JS's  .getTime() gives us the UTC in milleseconds. So here we turn it into a seconds-based
    // timestamp.
    //
    // If we send 'null', the server will respond with it's default "last 30 days" of transactions.
    let startDateUTCSeconds = startDate;
    let endDateUTCSeconds = endDate;

    if (startDate) {
      startDateUTCSeconds = Math.floor(startDate / 1000);
    }

    if (endDate) {
      endDateUTCSeconds = Math.floor(endDate / 1000);
    }

    // Let the state know we are fetching.
    dispatch({ type: types.FETCH_TRANSACTIONS });

    request
      .get('/api/cash/transactions/')
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        Accept: 'application/json',
      })
      .query({
        start_ts: startDateUTCSeconds,
        end_ts: endDateUTCSeconds,
      })
      .end((err, res) => {
        if (err) {
          dispatch(addMessage({
            type: types.ADD_MESSAGE,
            header: 'Could not fetch transactions',
            content: 'Start date is a later time than end date',
            level: 'warning',
            ttl: 3000,
          }));
          return dispatch(fetchTransactionsFail(err));
        }

        return dispatch(fetchTransactionsSuccess(res.body));
      }

    );
  };
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
