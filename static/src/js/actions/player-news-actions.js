import log from '../lib/logging';
import * as types from '../action-types.js';
import request from 'superagent';
import { normalize, Schema, arrayOf } from 'normalizr';
const playerNewsSchema = new Schema('playerNews', {
  idAttribute: 'id',
});


/**
 * Player News fetching actions.
 * /api/sports/player/news/{sport}/{optional-player-id}/
 */

function fetchingPlayerNews() {
  return {
    type: types.FETCHING_PLAYER_NEWS,
  };
}

function fetchPlayerNewsSuccess(body) {
  return {
    type: types.FETCH_PLAYER_NEWS_SUCCESS,
    sport: body.sport,
    playerNews: body.playerNews,
  };
}

function fetchPlayerNewsFail(ex) {
  log.error(ex);
  return {
    type: types.FETCH_PLAYER_NEWS_FAIL,
    ex,
  };
}


// Do we need to fetch the specified player news items?
function shouldFetchPlayerNews(state, sport) {
  const news = state.playerNews;

  if (news[sport] && Object.keys(news[sport]).length > 0) {
    // do we have any playerNews for the sport in the store, if so, is it empty?
    return false;
  } else if (news.isFetching) {
    // are we currently fetching it?
    return false;
  }

  // Default to true.
  return true;
}


function fetchPlayerNews(sport) {
  return dispatch => {
    // update the fetching state.
    dispatch(fetchingPlayerNews());

    return new Promise((resolve, reject) => {
      request
      .get(`/api/sports/player/news/${sport}/`)
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        Accept: 'application/json',
      })
      .end((err, res) => {
        if (err) {
          dispatch(fetchPlayerNewsFail(err));
          reject(err);
        } else {
          const normalizedPlayerNews = normalize(
            res.body,
            arrayOf(playerNewsSchema)
          );

          dispatch(fetchPlayerNewsSuccess({
            sport,
            playerNews: normalizedPlayerNews.entities.playerNews,
          }));

          resolve(res);
        }
      });
    });
  };
}


export function fetchPlayerNewsIfNeeded(sport) {
  return (dispatch, getState) => {
    if (shouldFetchPlayerNews(getState(), sport)) {
      return dispatch(fetchPlayerNews(sport));
    }

    return Promise.resolve();
  };
}
