import update from 'react-addons-update';
import * as ActionTypes from '../action-types';


// shortcut method to $set new state if the key doesn't exist, otherwise $merges the properties in to existing
const setOrMerge = (state, action, newProps) => {
  // if contest does not exist, then $set to create
  if (action.id in state === false) {
    return update(state, {
      [action.id]: {
        $set: newProps,
      },
    });
  }

  // otherwise merge
  return update(state, {
    [action.id]: {
      $merge: newProps,
    },
  });
};


module.exports = (state = {}, action) => {
  let newProps = {};

  switch (action.type) {
    case ActionTypes.REQUEST_LIVE_CONTEST_INFO:
      newProps = {
        id: action.id,
        isFetchingInfo: true,
        hasRelatedInfo: false,
      };

      return setOrMerge(state, action, newProps);


    case ActionTypes.RECEIVE_LIVE_CONTEST_INFO:
      return update(state, {
        [action.id]: {
          $merge: {
            info: action.info,
            expiresAt: action.expiresAt,
            isFetchingInfo: false,
          },
        },
      });


    case ActionTypes.REQUEST_LIVE_CONTEST_LINEUPS:
      newProps = {
        id: action.id,
        isFetchingLineups: true,
        hasRelatedInfo: false,
        attemptExpiresAt: action.attemptExpiresAt,
      };

      return setOrMerge(state, action, newProps);


    case ActionTypes.RECEIVE_LIVE_CONTEST_LINEUPS:
      return update(state, {
        [action.id]: {
          $merge: {
            lineupBytes: action.lineupBytes,
            lineups: action.lineups,
            isFetchingLineups: false,
          },
        },
      });


    case ActionTypes.REQUEST_LIVE_CONTEST_LINEUPS_USERNAMES:
      newProps = {
        id: action.id,
        isFetchingLineupsUsernames: true,
      };

      return setOrMerge(state, action, newProps);


    case ActionTypes.RECEIVE_LIVE_CONTEST_LINEUPS_USERNAMES:
      newProps = {
        id: action.id,
        isFetchingLineupsUsernames: false,
        lineupsUsernames: action.lineupsUsernames,
      };

      return setOrMerge(state, action, newProps);

    case ActionTypes.CONFIRM_RELATED_LIVE_CONTEST_INFO:
      return update(state, {
        [action.id]: {
          $merge: {
            hasRelatedInfo: true,
          },
        },
      });


    default:
      return state;
  }
};
