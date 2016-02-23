import * as ActionTypes from '../action-types';
import { forEach as _forEach } from 'lodash';
import { merge as _merge } from 'lodash';
import update from 'react-addons-update';
import { dateNow } from '../lib/utils';


// shortcut method to $set new state if the key doesn't exist, otherwise $merges the properties in to existing
const setOrMerge = (state, action, props) => {
  // if does not exist, then $set to create
  if (action.id in state === false) {
    const newProps = _merge(
      {},
      {
        playersInfo: {},
        playersStats: {},
        boxScores: {},
        infoExpiresAt: dateNow(),
        fpExpiresAt: dateNow(),
        boxscoresExpiresAt: dateNow(),
      },
      props
    );

    return update(state, {
      [action.id]: {
        $set: newProps,
      },
    });
  }

  // otherwise merge
  return update(state, {
    [action.id]: {
      $merge: props,
    },
  });
};


// update initialState to be a function to get from localStorage if it exists
module.exports = (state = {}, action) => {
  let newProps = {};

  switch (action.type) {
    case ActionTypes.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP:
      return update(state, {
        [action.id]: {
          playersStats: {
            [action.playerId]: {
              $set: {
                fp: action.fp,
              },
            },
          },
        },
      });


    case ActionTypes.REQUEST_LIVE_DRAFT_GROUP_INFO:
      newProps = {
        id: action.id,
        isFetchingInfo: true,
        hasAllInfo: false,
        infoExpiresAt: action.expiresAt,
      };

      return setOrMerge(state, action, newProps);


    case ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_INFO:
      return update(state, {
        [action.id]: {
          $merge: {
            isFetchingInfo: false,
            infoExpiresAt: action.expiresAt,
            playersInfo: action.players,
            playersBySRID: action.playersBySRID,
            start: action.start,
            end: action.end,
            sport: action.sport,
          },
        },
      });


    case ActionTypes.REQUEST_LIVE_DRAFT_GROUP_FP:
      newProps = {
        id: action.id,
        isFetchingFP: true,
        fpExpiresAt: action.expiresAt,
      };

      return setOrMerge(state, action, newProps);


    case ActionTypes.RECEIVE_LIVE_DRAFT_GROUP_FP:
      return update(state, {
        [action.id]: {
          $merge: {
            isFetchingFP: false,
            fpExpiresAt: action.expiresAt,
            playersStats: action.players,
          },
        },
      });

    case ActionTypes.REQUEST_DRAFT_GROUP_BOXSCORES:
      newProps = {
        id: action.id,
        isFetchingBoxscores: true,
        boxscoresExpiresAt: action.expiresAt,
      };

      return setOrMerge(state, action, newProps);

    case ActionTypes.RECEIVE_DRAFT_GROUP_BOXSCORES:
      return update(state, {
        [action.id]: {
          $merge: {
            isFetchingBoxscores: false,
            boxscoresExpiresAt: action.expiresAt,
            boxScores: action.boxscores,
          },
        },
      });

    case ActionTypes.CONFIRM_LIVE_DRAFT_GROUP_STORED:
      return update(state, {
        [action.id]: {
          $merge: {
            hasAllInfo: true,
          },
        },
      });


    // in order to remove all the keys properly, we need to loop through and delete them
    case ActionTypes.REMOVE_LIVE_DRAFT_GROUPS:
      const newState = _merge({}, state);

      _forEach(state, (dg) => {
        if (action.ids.indexOf(dg.id) > -1) {
          delete newState[dg.id];
        }
      });

      return newState;


    default:
      return state;
  }
};
