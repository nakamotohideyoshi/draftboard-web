import update from 'react-addons-update';
import * as ActionTypes from '../action-types';
import merge from 'lodash/merge';
import { dateNow } from '../lib/utils';
import log from '../lib/logging';


// TODO remove this hardcode of nba
module.exports = (state = {
  games: {},
  types: ['nba', 'nhl', 'mlb', 'nfl'],
  nba: {
    gameIds: [],
    gamesExpireAt: dateNow(),
    teamsExpireAt: dateNow(),
    teams: {},
  },
  nfl: {
    gameIds: [],
    gamesExpireAt: dateNow(),
    teamsExpireAt: dateNow(),
    teams: {},
  },
  nhl: {
    gameIds: [],
    gamesExpireAt: dateNow(),
    teamsExpireAt: dateNow(),
    teams: {},
  },
  mlb: {
    gameIds: [],
    gamesExpireAt: dateNow(),
    teamsExpireAt: dateNow(),
    teams: {},
  },
}, action = {}) => {
  switch (action.type) {
    case ActionTypes.REQUEST_TEAMS:
      return update(state, {
        [action.sport]: {
          $merge: {
            teamsExpireAt: action.expiresAt,
          },
        },
      });

    case ActionTypes.RECEIVE_TEAMS: {
      const { teams } = action.response;

      if (Object.keys(teams).length === 0) return state;

      return update(state, {
        [action.response.sport]: {
          $merge: {
            teams,
            teamsExpireAt: action.expiresAt,
          },
        },
      });
    }

    case ActionTypes.REQUEST_GAMES:
      return update(state, {
        [action.sport]: {
          $merge: {
            gamesExpireAt: action.expiresAt,
          },
        },
      });

    case ActionTypes.RECEIVE_GAMES: {
      const { games, gameIds, sport } = action.response;

      if (gameIds.length === 0) return state;

      return update(state, {
        games: {
          $merge: games,
        },
        [sport]: {
          $merge: {
            gamesExpireAt: action.expiresAt,
          },
          gameIds: {
            $set: gameIds,
          },
        },
      });
    }
    case ActionTypes.UPDATE_GAME: {
      if (!(action.gameId in state.games)) {
        log.warn(`Game id ${action.gameId} does not exist in the state`);
        return state;
      }

      const newState = merge({}, state);

      newState.games[action.gameId] = merge(
        {},
        state.games[action.gameId],
        action.updatedFields
      );

      return newState;
    }

    default:
      return state;
  }
};
