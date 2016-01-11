"use strict";

import request from 'superagent';
import { normalize, Schema, arrayOf } from 'normalizr';

import ActionTypes from '../action-types';
import log from '../lib/logging';


function requestLineupUsernames(contestId) {
  log.debug('actionsLineupUsernames.requestLineupUsernames');

  return {
    contestId,
    type: ActionTypes.REQUEST_LINEUP_USERNAMES
  };
}


function receiveLineupUsernames(contestId, response) {
  log.debug('actionsLineupUsernames.receiveLineupUsernames');

  return {
    contestId,
    type: ActionTypes.RECEIVE_LINEUP_USERNAMES,
    lineups: response.lineups
  };
}


export function fetchLineupUsernames(contestId) {
  log.debug('actionsLineupUsernames.fetchLineupUsernames');

  return (dispatch, getState) => {
    dispatch(requestLineupUsernames(contestId));

    // TODO:
    //
    // request
    //   .get('/api/contest/lineup-usernames/' + contestId)
    //   .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
    //   .set('Accept', 'application/json')
    //   .end((err, res) => {
    //     if(err) {
    //       // TODO
    //     } else {
    //       dispatch(receiveLineups(contestId, res.body));
    //     }
    // });

    dispatch(receiveLineupUsernames(contestId, {
      lineups: {
        '1': 'usernamefoo',
        '2': 'usernamebar'
      }
    }));
  };
}
