import * as ActionTypes from '../action-types';
import filter from 'lodash/filter';
import orderBy from 'lodash/orderBy';
import map from 'lodash/map';
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
  return map(uniq, (pitch) => ({
    count: pitch.p_idx,
    outcome: (pitch.pitch_zone < 10) ? 'strike' : 'ball',
    speed: pitch.pitch_speed,
    type: sportConst.pitchTypes[pitch.pitch_type],
    zone: pitch.pitch_zone,
  }));
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
