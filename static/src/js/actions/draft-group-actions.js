import * as types from '../action-types.js'
import request from 'superagent'
// so we can use Promises
import 'babel-core/polyfill';
import {normalize, Schema, arrayOf} from 'normalizr'
import {fetchSportInjuries} from './injury-actions.js'
import {fetchFantasyHistory} from './fantasy-history-actions.js'
import {importLineup} from './lineup-actions.js'


const playerSchema = new Schema('players', {
  idAttribute: 'player_id'
})



export function updateFilter(filterName, filterProperty, match) {
  return {
    type: types.DRAFTGROUP_FILTER_CHANGED,
    filter: {
      filterName,
      filterProperty,
      match
    }
  }
}


export function setFocusedPlayer(playerId) {
  return (dispatch) => {
    dispatch({
      type: types.SET_FOCUSED_PLAYER,
      playerId
    });
  };
}


/**
 * Draft Group fetching actions
 * /api/draft-group/draftGroupId
 */
function fetchingDraftgroup() {
  return {
    type: types.FETCHING_DRAFT_GROUPS
  };
}

function fetchDraftgroupSuccess(body) {
  return {
    type: types.FETCH_DRAFTGROUP_SUCCESS,
    body
  };
}

function fetchDraftgroupFail(ex) {
  window.alert(ex)
  return {
    type: types.FETCH_DRAFTGROUP_FAIL,
    ex
  };
}

// Do we need to fetch the specified draft group?
function shouldFetchDraftGroup(state, draftGroupId) {
  const draftGroup = state.draftDraftGroup

  if (!draftGroup.id || draftGroupId !== draftGroup.id) {
    // do we have a draftgroup AND the right draftgroup in the store?
    return true
  } else if (draftGroup.isFetching) {
    // are we currently fetching it?
    return false
  } else {
    // Default to true.
    return true
  }
}

export function fetchDraftGroupIfNeeded(draftGroupId) {
  return (dispatch, getState) => {
    if(shouldFetchDraftGroup(getState(), draftGroupId)) {
      return dispatch(fetchDraftGroup(draftGroupId))
    } else {
      return Promise.resolve()
    }
  };
}

function fetchDraftGroup(draftGroupId) {
  return dispatch => {
    // update the fetching state.
    dispatch(fetchingDraftgroup())

    return new Promise((resolve, reject) => {
       request
      .get("/api/draft-group/" + draftGroupId + '/')
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'Accept': 'application/json'
      })
      .end(function(err, res) {
        if(err) {
          dispatch(fetchDraftgroupFail(err));
          reject(err)
        } else {
          // Now that we know which sport we're dealing with, fetch the injuries + fp history for
          // these players.
          dispatch(fetchFantasyHistory(res.body.sport))
          dispatch(fetchSportInjuries(res.body.sport))

          // Normalize player list by ID.
          const normalizedPlayers = normalize(
            res.body.players,
            arrayOf(playerSchema)
          )

          dispatch(fetchDraftgroupSuccess({
            players: normalizedPlayers.entities.players,
            start: res.body.start,
            end: res.body.end,
            sport: res.body.sport,
            id: res.body.pk
          }));

          resolve(res)
        }
      });
    });
  }
}



/**
 * Draft Group Box Score fetching Actions.
 * /api/draft-group/boxscores/${draftGroupId}/
 */

export function fetchDraftGroupBoxScores(draftGroupId) {
  return dispatch => {

    return new Promise((resolve, reject) => {
      request
      .get(`/api/draft-group/boxscores/${draftGroupId}/`)
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'Accept': 'application/json'
      })
      .end(function(err, res) {
        if(err) {
          window.alert('fetchDraftGroupBoxScores', err)
        } else {
          const fixtures = [{"model": "nba.gameboxscore", "pk": 361, "fields": {"home_id": 13, "home_scoring_json": "", "times_tied": 0, "quarter": "4.0", "srid_away": "583ec825-fb46-11e1-82cb-f4ce4684ea4c", "home_score": 0, "srid_home": "583ec7cd-fb46-11e1-82cb-f4ce4684ea4c", "srid_game": "0a02f948-bdcd-44ca-98c9-3fe756c819e5", "away_scoring_json": "", "coverage": "full", "home_type": 64, "attendance": 18165, "title": "", "away_type": 64, "clock": "00:00", "away_score": 0, "lead_changes": 3, "duration": "2:14", "created": "2015-12-02T04:13:27.410Z", "away_id": 26, "status": "closed"}}, {"model": "nba.gameboxscore", "pk": 362, "fields": {"home_id": 12, "home_scoring_json": "", "times_tied": 4, "quarter": "4.0", "srid_away": "583ed056-fb46-11e1-82cb-f4ce4684ea4c", "home_score": 0, "srid_home": "583ec773-fb46-11e1-82cb-f4ce4684ea4c", "srid_game": "194d4daf-cfa2-449f-b418-e87a9592d616", "away_scoring_json": "", "coverage": "full", "home_type": 64, "attendance": 20562, "title": "", "away_type": 64, "clock": "00:00", "away_score": 0, "lead_changes": 4, "duration": "2:20", "created": "2015-12-02T04:13:27.415Z", "away_id": 19, "status": "closed"}}, {"model": "nba.gameboxscore", "pk": 363, "fields": {"home_id": 8, "home_scoring_json": "", "times_tied": 1, "quarter": "4.0", "srid_away": "583ecb3a-fb46-11e1-82cb-f4ce4684ea4c", "home_score": 0, "srid_home": "583ec9d6-fb46-11e1-82cb-f4ce4684ea4c", "srid_game": "7398e78d-8047-4e21-9c33-d6fc0ae406d2", "away_scoring_json": "", "coverage": "full", "home_type": 64, "attendance": 13319, "title": "", "away_type": 64, "clock": "00:00", "away_score": 0, "lead_changes": 6, "duration": "2:09", "created": "2015-12-02T04:13:27.420Z", "away_id": 22, "status": "closed"}}, {"model": "nba.gameboxscore", "pk": 364, "fields": {"home_id": 21, "home_scoring_json": "", "times_tied": 2, "quarter": "4.0", "srid_away": "583ecfff-fb46-11e1-82cb-f4ce4684ea4c", "home_score": 0, "srid_home": "583eca88-fb46-11e1-82cb-f4ce4684ea4c", "srid_game": "c79c4d00-ac19-4f45-b9ee-bad6a9b98aa2", "away_scoring_json": "", "coverage": "full", "home_type": 64, "attendance": 16415, "title": "", "away_type": 64, "clock": "00:00", "away_score": 0, "lead_changes": 2, "duration": "2:09", "created": "2015-12-02T04:13:27.425Z", "away_id": 18, "status": "closed"}}, {"model": "nba.gameboxscore", "pk": 365, "fields": {"home_id": 20, "home_scoring_json": "", "times_tied": 7, "quarter": "4.0", "srid_away": "583ed157-fb46-11e1-82cb-f4ce4684ea4c", "home_score": 0, "srid_home": "583ed102-fb46-11e1-82cb-f4ce4684ea4c", "srid_game": "601d922e-e4f2-400f-882e-3b939a20e2ba", "away_scoring_json": "", "coverage": "full", "home_type": 64, "attendance": 13925, "title": "", "away_type": 64, "clock": "00:00", "away_score": 0, "lead_changes": 12, "duration": "2:04", "created": "2015-12-02T04:13:27.429Z", "away_id": 5, "status": "closed"}}, {"model": "nba.gameboxscore", "pk": 366, "fields": {"home_id": 30, "home_scoring_json": "", "times_tied": 0, "quarter": "4.0", "srid_away": "583ece50-fb46-11e1-82cb-f4ce4684ea4c", "home_score": 0, "srid_home": "583ed0ac-fb46-11e1-82cb-f4ce4684ea4c", "srid_game": "66c735af-f87f-4cae-885e-75c912b4bf91", "away_scoring_json": "", "coverage": "full", "home_type": 64, "attendance": 16505, "title": "", "away_type": 64, "clock": "00:00", "away_score": 0, "lead_changes": 1, "duration": "2:12", "created": "2015-12-02T04:13:27.433Z", "away_id": 17, "status": "closed"}}]
          console.log(res.body)
          console.error('fetchDraftGroupBoxScores action is loading fixture data!')
          dispatch(fetchDraftGroupBoxScoresSuccess(fixtures))
        }
      })
    })

  }
}


function fetchDraftGroupBoxScoresSuccess(body) {
  return {
    type: types.FETCH_DRAFTGROUP_BOXSCORES_SUCCESS,
    boxScores: body
  };

}
