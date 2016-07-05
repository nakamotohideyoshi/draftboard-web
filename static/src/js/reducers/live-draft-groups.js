import * as ActionTypes from '../action-types';
import forEach from 'lodash/forEach';
import log from '../lib/logging';
import merge from 'lodash/merge';
import Raven from 'raven-js';
import update from 'react-addons-update';
import { dateNow } from '../lib/utils';


// shortcut method to $set new state if the key doesn't exist, otherwise $merges the properties in to existing
const setOrMerge = (state, id, props) => {
  // if does not exist, then $set to create
  if (id in state === false) {
    const newProps = merge(
      {},
      {
        boxScores: {},
        boxscoresExpiresAt: dateNow(),
        fpExpiresAt: dateNow(),
        hasAllInfo: false,
        infoExpiresAt: dateNow(),
        playersInfo: {},
        playersStats: {},
      },
      props
    );

    return update(state, {
      [id]: {
        $set: newProps,
      },
    });
  }

  // otherwise merge
  return update(state, {
    [id]: {
      $merge: props,
    },
  });
};


// update initialState to be a function to get from localStorage if it exists
module.exports = (state = {}, action = {}) => {
  let newProps = {};

  switch (action.type) {

    case ActionTypes.CONFIRM_LIVE_DRAFT_GROUP_STORED:
      // don't confirm if there is no draft group
      if (!(action.id in state)) return state;

      return update(state, {
        [action.id]: {
          $merge: {
            hasAllInfo: true,
          },
        },
      });


    case ActionTypes.LIVE_DRAFT_GROUP__INFO__REQUEST:
      newProps = {
        id: action.id,
        hasAllInfo: false,
        infoExpiresAt: action.expiresAt,
      };

      return setOrMerge(state, action.id, newProps);


    case ActionTypes.LIVE_DRAFT_GROUP__INFO__RECEIVE: {
      const { response } = action;

      newProps = {
        infoExpiresAt: action.expiresAt,
        id: response.id,
        playersInfo: response.players,
        start: response.start,
        end: response.end,
        sport: response.sport,
      };

      return setOrMerge(state, response.id, newProps);
    }


    case ActionTypes.REQUEST_LIVE_DRAFT_GROUP_FP:
      newProps = {
        id: action.id,
        fpExpiresAt: action.expiresAt,
      };

      return setOrMerge(state, action.id, newProps);


    case ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_FP: {
      const { response } = action;

      newProps = {
        id: response.id,
        fpExpiresAt: action.expiresAt,
        playersStats: action.response.players,
      };

      return setOrMerge(state, response.id, newProps);
    }


    case ActionTypes.REQUEST_DRAFT_GROUP_BOXSCORES:
      newProps = {
        id: action.id,
        boxscoresExpiresAt: action.expiresAt,
      };

      return setOrMerge(state, action.id, newProps);

    case ActionTypes.RECEIVE_DRAFT_GROUP_BOXSCORES: {
      const { response } = action;

      newProps = {
        id: response.id,
        boxscoresExpiresAt: action.expiresAt,
        boxScores: action.response.boxscores,
      };

      return setOrMerge(state, response.id, newProps);
    }


    // in order to remove all the keys properly, we need to loop through and delete them
    case ActionTypes.REMOVE_LIVE_DRAFT_GROUPS: {
      const newState = merge({}, state);

      forEach(state, (dg) => {
        if (action.ids.indexOf(dg.id) > -1) delete newState[dg.id];
      });

      return newState;
    }


    case ActionTypes.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP:
      // ignore if we aren't watching this draft group
      if (!state[action.id]) return state;

      if (state[action.id].playersStats.hasOwnProperty(action.playerId) === false) {
        const reasonWhy = `No player stats for ${action.playerId} in draft group ${action.id}`;
        const why = {
          extra: {
            action,
            reasonWhy,
          },
        };

        Raven.captureMessage('UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP failed', why);
        log.info(reasonWhy);

        return state;
      }

      return update(state, {
        [action.id]: {
          playersStats: {
            [action.playerId]: {
              $merge: {
                fp: action.fp,
              },
            },
          },
        },
      });


    default:
      return state;
  }
};
