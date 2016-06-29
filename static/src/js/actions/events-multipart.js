import * as ActionTypes from '../action-types';
import { batchActions } from 'redux-batched-actions';
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
