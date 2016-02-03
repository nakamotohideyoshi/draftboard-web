import update from 'react-addons-update';
import * as ActionTypes from '../action-types';
import moment from 'moment'


// TODO remove this hardcode of nba
module.exports = (state = {
  games: {},
  types: ['nba'],
  nba: {
    gameIds: [],
    isFetchingTeams: false,
    isFetchingGames: false,
    gamesExpireAt: moment(),
    teamsExpireAt: moment(),
  },
}, action) => {
  switch (action.type) {
    case ActionTypes.REQUEST_TEAMS:
      return update(state, {
        [action.sport]: {
          $merge: {
            isFetchingTeams: true,
          },
        },
      });

    case ActionTypes.RECEIVE_TEAMS:
      return update(state, {
        [action.sport]: {
          $merge: {
            teams: action.teams,
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
          },
        },
      });

    case ActionTypes.RECEIVE_GAMES:
      return update(state, {
        games: {
          $merge: action.games,
        },
        [action.sport]: {
          $merge: {
            gameIds: action.gameIds,
            isFetchingGames: false,
            gamesExpireAt: action.expiresAt,
          },
        },
      });

    case ActionTypes.UPDATE_GAME:
      return update(state, {
        games: {
          [action.gameId]: {
            boxscore: {
              $merge: action.updatedGameFields,
            },
          },
        },
      });

    default:
      return state;
  }
};
