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
              image: "../img/blocks/results/avatar.png",
              position: "pg"
            },
            {
              id: 2,
              name: "name.1",
              score: 70,
              image: "../img/blocks/results/avatar.png",
              position: "pg"
            }
          ],
          contests: [
            {
              id: 1,
              factor: 2,
              title: "$25 - Anonymous Head-to-Head",
              place: 16,
              prize: "$20"
            },
            {
              id: 2,
              factor: 1,
              title: "$10,000 - Guaranteed Tier Anonymous Head-to-Head",
              place: 1,
              prize: "$500"
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
