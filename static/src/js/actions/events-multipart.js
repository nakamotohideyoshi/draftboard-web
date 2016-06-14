import * as ActionTypes from '../action-types';
import filter from 'lodash/filter';
import orderBy from 'lodash/orderBy';
import map from 'lodash/map';
import random from 'lodash/random';
import uniqBy from 'lodash/uniq';
import { batchActions } from 'redux-batched-actions';
import { SPORT_CONST } from './sports';
import log from '../lib/logging';

// dispatch to reducer methods

const deleteMultipartEvent = (key) => ({
  type: ActionTypes.EVENT_MULTIPART_DELETE,
  key,
});

const deleteWatchablePlayers = (players) => ({
  type: ActionTypes.EVENT_MULTIPART_OMIT_PLAYERS,
  players,
});

const setEventMultipart = (key, value) => ({
  type: ActionTypes.EVENT_MULTIPART_SET,
  key,
  value,
});

const mergeWatchablePlayers = (players, eventId) => ({
  type: ActionTypes.EVENT_MULTIPART_MERGE_PLAYERS,
  players,
  eventId,
});


// helper methods


export const consolidateZonePitches = (zonePitches) => {
  const sportConst = SPORT_CONST.mlb;
  const filtered = filter(zonePitches, (pitch) => pitch.hasOwnProperty('pitch_speed'));
  const sorted = orderBy(filtered, 'dd_updated__id');
  const uniq = uniqBy(sorted, 'p_idx');

  // could make this dynamic, but faster if we just write it out for now
  return map(uniq, (pitch) => {
    // randomize position of pitch within zone
    const zone = pitch.pitch_zone;
    let left = 0;
    let top = 0;

    // left
    switch (zone) {
      case 1:
      case 4:
      case 7:
        left = random(-4, 22);
        break;
      case 2:
      case 5:
      case 8:
        left = random(30, 55);
        break;
      case 3:
      case 6:
      case 9:
        left = random(64, 88);
        break;
      case 10:
        left = random(98, 108);
        break;
      case 12:
        left = random(-24, -12);
        break;
      case 11:
      case 13:
        left = random(-2, 88);
        break;
      default:
        left = 0;
    }

    // top
    switch (zone) {
      case 1:
      case 2:
      case 3:
        top = random(-2, 23);
        break;
      case 4:
      case 5:
      case 6:
        top = random(31, 56);
        break;
      case 7:
      case 8:
      case 9:
        top = random(65, 90);
        break;
      case 11:
        top = random(98, 108);
        break;
      case 13:
        top = random(-20, -10);
        break;
      case 10:
      case 12:
        top = random(-2, 90);
        break;
      default:
        top = 0;
    }

    return {
      count: pitch.p_idx,
      outcome: (pitch.pitch_zone < 10) ? 'strike' : 'ball',
      speed: pitch.pitch_speed,
      type: sportConst.pitchTypes[pitch.pitch_type],
      zone: pitch.pitch_zone,
      left,
      top,
    };
  });
};


/**
 * Helper method to convert an object of pitch types into a readable sentence
 * Example pitchCount:
 * "count__list": {
 *    "pitch_count": 5,
 *    "strikes": 1,
 *    "balls": 3,
 *    "outs": 3
 *  },
 * @param  {object} pitchCount Types of pitches and their count
 * @return {string}            Human readable pitch count
 */
export const stringifyAtBat = (pitchCount) =>
  `${pitchCount.balls}B/${pitchCount.strikes}S - ${pitchCount.outs} Outs`;


/**
 * Returns string stating when event occurred in game
 * @param  {number} inning Loose number of inning, eg '5.0'
 * @param  {string} half   Bottom or top of inning, denoted with 'B', 'T', respectively
 * @return {string}        Readable version of when, eg 'Bottom of 5th', or false if it has not started
 */
export const stringifyMLBWhen = (inning, half) => {
  const when = (half === 'B') ? 'Bottom' : 'Top';
  const inningInt = parseInt(inning, 10) || 0;

  if (isNaN(inningInt)) return false;

  let ordinal = '';
  switch (inningInt) {
    case 1:
      ordinal = 'st';
      break;
    case 2:
      ordinal = 'nd';
      break;
    case 3:
      ordinal = 'rd';
      break;
    default:
      ordinal = 'th';
  }

  if (half) {
    return `${when} of ${inningInt}${ordinal}`;
  }

  return `${inningInt}${ordinal}`;
};


// primary methods (mainly exported, some needed in there to have proper init of const)


/**
 * When a multipart event is complete (when there's an outcome_id in the event), remove watchable players and event
 * NOTE: this method must be dispached by redux store
 * @param  {string} key       Unique ID. Correlates to at_bat__id for mlb, drive__id for nfl
 * @param  {object} players   List of players to remove
 * @return {thunk}            Method of action creator
 */
export const removeEventMultipart = (key, players = []) => (dispatch, getState) => {
  log.trace('removeEventMultipart', key, players);

  const state = getState();
  const actions = [];

  if (players.length > 0) {
    actions.push(deleteWatchablePlayers(players));
  }

  // only delete event if it exists
  if (state.eventsMultipart.events.hasOwnProperty(key)) {
    actions.push(deleteMultipartEvent(key));
  }

  return dispatch(batchActions(actions));
};

/**
 * Store a multipart event, by either adding new or updating existing
 * NOTE: this method must be dispached by redux store
 * @param  {string} key       Unique ID. Correlates to at_bat__id for mlb, drive__id for nfl
 * @param  {object} value     All relevant data related to event
 * @param  {array}  players   List of relevant players to watch
 * @return {thunk}            Method of action creator
 */
export const storeEventMultipart = (key, value, players = []) => (dispatch) => {
  const actions = [setEventMultipart(key, value)];

  if (players.length > 0) {
    actions.push(mergeWatchablePlayers(players, key));
  }

  return dispatch(batchActions(actions));
};
