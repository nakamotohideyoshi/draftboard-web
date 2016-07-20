import update from 'react-addons-update';
import * as ActionTypes from '../action-types';
import merge from 'lodash/merge';
import { dateNow } from '../lib/utils';


// TODO remove this hardcode of nba
module.exports = (state = {
  games: {},
  types: ['nba', 'nhl', 'mlb', 'nfl'],
  nba: {
    gameIds: [],
    isFetchingTeams: false,
    isFetchingGames: false,
    gamesExpireAt: dateNow(),
    teamsExpireAt: dateNow(),
  },
  nfl: {
    gameIds: [],
    isFetchingTeams: false,
    isFetchingGames: false,
    gamesExpireAt: dateNow(),
    teamsExpireAt: dateNow(),
  },
  nhl: {
    gameIds: [],
    isFetchingTeams: false,
    isFetchingGames: false,
    gamesExpireAt: dateNow(),
    teamsExpireAt: dateNow(),
  },
  mlb: {
    gameIds: [],
    isFetchingTeams: false,
    isFetchingGames: false,
    gamesExpireAt: dateNow(),
    teamsExpireAt: dateNow(),
  },
}, action = {}) => {
  switch (action.type) {
    case ActionTypes.REQUEST_TEAMS:
      return update(state, {
        [action.sport]: {
          $merge: {
            isFetchingTeams: true,
            teamsExpireAt: action.expiresAt,
          },
        },
      });

    case ActionTypes.RECEIVE_TEAMS:
      return update(state, {
        [action.sport]: {
          $merge: {
            teams: action.response.teams,
            isFetchingTeams: false,
            teamsExpireAt: action.expiresAt,
          },
        },
      });

    case ActionTypes.REQUEST_GAMES:
      return update(state, {
        [action.sport]: {
          $merge: {
            isFetchingGames: true,
            gamesExpireAt: action.expiresAt,
          },
        },
      });

    case ActionTypes.RECEIVE_GAMES:
      return update(state, {
        games: {
          $merge: action.response.games,
        },
        [action.sport]: {
          $merge: {
            isFetchingGames: false,
            gamesExpireAt: action.expiresAt,
          },
          gameIds: {
            $set: action.response.gameIds,
          },
        },
      });

    case ActionTypes.UPDATE_GAME:
      if (!(action.gameId in state.games)) break;

      return update(state, {
        games: {
          [action.gameId]: {
            $set: merge({}, state.games[action.gameId], action.updatedFields),
          },
        },
      });

    default:
      return state;
  }
};
