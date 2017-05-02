import * as ActionTypes from '../action-types';
import log from '../lib/logging';
import { CALL_API } from '../middleware/api';
import { dateNow } from '../lib/utils';

// get custom logger for actions
const logAction = log.getLogger('action');

/**
 * Player history fetching actions.
 *
 * This gets the players REAL LIFE box score history for the past X number of games.
 * It's used in the draft + live sections to populate the player detail pane stats.
 **/
const fetchSinglePlayerBoxScoreHistory = (sport, id) => ({
  [CALL_API]: {
    types: [
      ActionTypes.PLAYER_HISTORY_SINGLE__REQUEST,
      ActionTypes.PLAYER_HISTORY_SINGLE__RECEIVE,
      ActionTypes.ADD_MESSAGE,
    ],
    expiresAt: dateNow() + 1000 * 60 * 60 * 12,  // 12 hours, aka end of night
    endpoint: `/api/sports/player/history/${sport}/20/${id}/`,  // fetch the average history of last 20 games
    requestFields: { sport, id },
    callback: (json) => ({
      id,
      sport,
      fields: json[0],
    }),
  },
});

export const fetchSinglePlayerNews = (sport, playerSrid) => ({
  [CALL_API]: {
    types: [
      ActionTypes.PLAYER_NEWS_SINGLE__REQUEST,
      ActionTypes.PLAYER_NEWS_SINGLE__RECEIVE,
      ActionTypes.ADD_MESSAGE,
    ],
    endpoint: `/api/sports/updates/player/${playerSrid}?category=news/`,  // fetch the news and analysis
    requestFields: { sport, playerSrid },
    callback: (json) => ({
      fields: json,
    }),
  },
});


/**
 * Quick check to see if we should fetch the history of a player
 * Essentially, fetch if it doesn't exist
 * @param  {object} state Redux state
 * @param  {string} sport Sport to filter by
 * @param  {number} id    Django model ID for the player
 * @return {boolean}      True if we should fetch
 */
const shouldFetchSinglePlayerBoxScoreHistory = (state, sport, id) => !(id in state.playerBoxScoreHistory[sport]);


export const fetchSinglePlayerBoxScoreHistoryIfNeeded = (sport, id) => (dispatch, getState) => {
  logAction.info('actions.fetchSinglePlayerBoxScoreHistoryIfNeeded', sport, id);

  if (shouldFetchSinglePlayerBoxScoreHistory(getState(), sport, id)) {
    return dispatch(fetchSinglePlayerBoxScoreHistory(sport, id));
  }

  return Promise.resolve();
};
