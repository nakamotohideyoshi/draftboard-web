import request from 'superagent';
import Cookies from 'js-cookie';
import log from '../lib/logging';
import * as actionTypes from '../action-types';


function fetchContestPoolEntriesFail(err) {
  return {
    type: actionTypes.FETCH_CONTEST_POOL_ENTRIES_FAIL,
    err,
  };
}


function fetchContestPoolEntriesSucess(body) {
  return {
    type: actionTypes.FETCH_CONTEST_POOL_ENTRIES_SUCCESS,
    body,
  };
}


/**
 * Get the user's contest pool entries.
 */
export function fetchContestPoolEntries() {
  return (dispatch) => {
    // Tell the store we are currently fetching entries.
    dispatch({ type: actionTypes.FETCHING_CONTEST_POOL_ENTRIES });

    return new Promise((resolve, reject) => {
      request
      .get('/api/contest/contest-pools/entries/')
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'X-CSRFToken': Cookies.get('csrftoken'),
        Accept: 'application/json',
      })
      .end((err, res) => {
        if (err) {
          log.error(err);
          dispatch(fetchContestPoolEntriesFail(err));
          reject(err);
        } else {
          dispatch(fetchContestPoolEntriesSucess(res.body));
          resolve(res);
        }
      });
    });
  };
}
