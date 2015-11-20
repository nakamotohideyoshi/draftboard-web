"use strict";

import request from 'superagent';
import { normalize, Schema, arrayOf } from 'normalizr';

import ActionTypes from '../action-types';
import log from '../lib/logging';


function requestLineups(id) {
  log.debug('actionsResults.requestLineups');

  return {
    id,
    type: ActionTypes.REQUEST_LINEUPS_RESULTS
  };
}


function receiveLineups(id, response) {
  log.debug('actionsResults.receiveLineups');

  return {
    id,
    type: ActionTypes.RECEIVE_LINEUPS_RESULTS,
    stats: response.stats,
    lineups: response.lineups
  };
}


export function fetchLineups(id, date) {
  log.debug('actionsResults.fetchLineups');

  return (dispatch, getState) => {
    dispatch(requestLineups(id));

    // TODO:
    //
    // request
    //   .get('/prize/' + id)
    //   .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
    //   .set('Accept', 'application/json')
    //   .end((err, res) => {
    //     if(err) {
    //       // TODO
    //     } else {
    //       dispatch(receiveLineups(id, res.body));
    //     }
    // });

    dispatch(receiveLineups(id, {
      stats: {
        winnings: '0$',
        possible: '$542,50',
        fees: '$220',
        entries: 24,
        contests: 18
      },
      lineups: [
        {
          id: 1,
          name: "Warrior's Stack",
          players: [
            {
              id: 1,
              name: "name.1",
              score: 70,
              image: "image.1",
              position: "pg"
            },
            {
              id: 2,
              name: "name.1",
              score: 70,
              image: "image.1",
              position: "pg"
            }
          ],
          stats: {
            fees: '$120',
            won: '$1,850.50',
            entries: 22
          }
        }
      ]
    }));
  };
}
