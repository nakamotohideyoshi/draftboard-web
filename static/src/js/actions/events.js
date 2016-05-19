import * as ActionTypes from '../action-types';
import log from '../lib/logging';
import store from '../store';
import { filter as _filter } from 'lodash';
import { forEach as _forEach } from 'lodash';
import { GAME_DURATIONS } from './sports';
import { stringifyAtBat, stringifyMLBWhen, consolidateZonePitches, removeEventMultipart } from './events-multipart';
import {
  watchingMyLineupSelector,
  relevantGamesPlayersSelector,
  watchingOpponentLineupSelector,
} from '../selectors/watching';
import { intersection as _intersection } from 'lodash';
import { merge as _merge } from 'lodash';
import { storeEventMultipart } from './events-multipart';
import { updateGameTeam } from './sports';
import { updateGameTime } from './sports';
import { updatePlayerStats } from './live-draft-groups';
import { batchActions } from 'redux-batched-actions';

const addAnimationEvent = (key, value) => ({
  type: ActionTypes.EVENT_ADD_ANIMATION,
  key,
  value,
});

const addPlayerEventDescription = (key, value) => ({
  type: ActionTypes.EVENT_PLAYER_ADD_DESCRIPTION,
  key,
  value,
});

const differencePlayersPlaying = (players) => ({
  type: ActionTypes.EVENT_DIFFERENCE_PLAYERS_PLAYING,
  players,
});

const unionPlayersPlaying = (players) => ({
  type: ActionTypes.EVENT_UNION_PLAYERS_PLAYING,
  players,
});

const pushEvent = (gameId, event) => ({
  type: ActionTypes.EVENT_GAME_QUEUE_PUSH,
  gameId,
  event,
});

const eventsQueueAddGame = (gameId) => ({
  type: ActionTypes.EVENT_ADD_GAME_QUEUE,
  gameId,
});

export const removeAnimationEvent = (key) => ({
  type: ActionTypes.EVENT_REMOVE_ANIMATION,
  key,
});

const removePlayerEventDescription = (key) => ({
  type: ActionTypes.EVENT_PLAYER_REMOVE_DESCRIPTION,
  key,
});

const unshiftPlayerHistory = (key, value) => ({
  type: ActionTypes.EVENT_UNSHIFT_PLAYER_HISTORY,
  key,
  value,
});

const showThenHidePlayerEventDescription = (key, value) => (dispatch) => {
  dispatch(addPlayerEventDescription(key, value));

  setTimeout(() => {
    dispatch(removePlayerEventDescription(key));
  }, 3000);
};

/**
 * Store a multipart event, by either adding new or updating existing
 * - Only used internally, exported for testing purposes
 * - This method must be dispached by redux store
 * @param  {string} key       Unique ID. Correlates to at_bat__id for mlb, drive__id for nfl
 * @param  {object} value     All relevant data related to event
 * @param  {array}  players   List of relevant players to watch
 * @return {thunk}            Method of action creator
 */
export const storeEvent = (gameId, event) => (dispatch, getState) => {
  const state = getState();
  const actions = [];

  // if there's no game queue, add it first
  if (state.events.gamesQueue.hasOwnProperty(gameId) === false) {
    actions.push(eventsQueueAddGame(gameId));
  }

  actions.push(pushEvent(gameId, event));

  return dispatch(batchActions(actions));
};

const updatePBPPlayersStats = (playersStats) => {
  const state = store.getState();
  const myLineup = watchingMyLineupSelector(state);
  const watching = state.watching;

  // don't update if we aren't ready
  if (watching.myLineupId === null || myLineup.isLoading === true) return false;

  const draftGroupId = myLineup.draftGroupId;

  _forEach(playersStats, (playerStats) => {
    const playerId = playerStats.fields.player_id;
    log.info('updatePBPPlayersStats - linked pbp - updatePlayerStats()', playerId);

    if (state.liveDraftGroups[draftGroupId].playersStats.hasOwnProperty(playerId)) {
      store.dispatch(updatePlayerStats(
        playerStats.fields.player_id,
        playerStats,
        myLineup.draftGroupId
      ));
    }
  });
};

/**
 * Dispatch information to reducer that we have completed getting all information related to the entries
 * Used to make the components aware tht we have finished pulling information.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
export const shiftGameQueueEvent = (gameId) => ({
  gameId,
  type: ActionTypes.EVENT_SHIFT_GAME_QUEUE,
});

const whichSide = (watching, relevantPlayersInEvent, opponentLineup, relevantGamesPlayers) => {
  // determine what color the animation should be, based on which lineup(s) the player(s) are in
  if (watching.opponentLineupId && opponentLineup.isLoading === false) {
    const rosterBySRID = opponentLineup.rosterBySRID;
    const playersInBothLineups = relevantGamesPlayers.playersInBothLineups;

    if (_intersection(rosterBySRID, relevantPlayersInEvent).length > 0) {
      return 'opponent';
    }
    if (_intersection(playersInBothLineups, relevantPlayersInEvent).length > 0) {
      return 'both';
    }
  }

  return 'mine';
};

export const showAnimationEventResults = (animationEvent) => {
  log.debug('setTimeout - show the results');

  store.dispatch(differencePlayersPlaying(animationEvent.relevantPlayersInEvent));

  const eventPBP = animationEvent.eventPBP;

  // show event beside player and in their history
  _forEach(animationEvent.relevantPlayersInEvent, (playerId) => {
    const eventDescription = {
      points: null,
      info: eventPBP.description,
      when: eventPBP.clock,
      id: animationEvent.id,
      playerId,
    };

    store.dispatch(unshiftPlayerHistory(playerId, eventDescription));
    store.dispatch(showThenHidePlayerEventDescription(playerId, eventDescription));
  });

  // update player stats if we have them
  updatePBPPlayersStats(animationEvent.playersStats);
};

/*
 * Show a game event from a Pusher pbp call. If this is a multipart, then add there, otherwise just add as normal event
 * @param  {object} eventCall The event call to parse for information
 */
const showGameEvent = (eventCall, state) => {
  log.trace('showGameEvent', eventCall, state);

  // get just pbp data if linked
  const eventPBP = eventCall.pbp || eventCall;

  const opponentLineup = watchingOpponentLineupSelector(state);
  const relevantGamesPlayers = relevantGamesPlayersSelector(state);
  const watching = state.watching;
  const eventPlayers = eventCall.addedData.eventPlayers;
  const relevantPlayersInEvent = _intersection(relevantGamesPlayers.relevantItems.players, eventPlayers);
  const sport = eventCall.addedData.sport;
  const sportConst = GAME_DURATIONS[sport];

  // relevant information for court animation
  let animationEvent;

  switch (sport) {
    case 'mlb':
      animationEvent = {
        eventPBP,
        eventCall,
        gameId: eventPBP.game__id,
        id: eventPBP.id,
        playersStats: eventCall.stats || {},
        relevantPlayersInEvent,
        whichSide: whichSide(watching, relevantPlayersInEvent, opponentLineup, relevantGamesPlayers),
      };

      // if we need to show as an event, push that out first
      if (eventPBP.hasOwnProperty('at_bat__id') === false || eventPBP.flags__list.is_ab_over) {
        store.dispatch(addAnimationEvent(animationEvent.id, animationEvent));
      }

      // if multipart
      if (eventPBP.hasOwnProperty('at_bat__id')) {
        // remove in 5 seconds if the multievent is over
        if (eventPBP.flags__list.is_ab_over === 'true') {
          log.info('At bat over for ', relevantPlayersInEvent);
          const boxscore = state.sports.games[animationEvent.gameId].boxscore;

          setTimeout(
            () => {
              store.dispatch(removeEventMultipart(eventPBP.at_bat__id, relevantPlayersInEvent));

              const actions = [];
              _forEach(animationEvent.relevantPlayersInEvent, (playerId) => {
                const eventDescription = {
                  points: null,
                  info: eventCall.at_bat.description,
                  when: stringifyMLBWhen(boxscore.inning, boxscore.inning_half),
                  id: animationEvent.id,
                  playerId,
                };

                actions.push(unshiftPlayerHistory(playerId, eventDescription));
              });

              store.dispatch(batchActions(actions));
            },
            5000
          );
        }

        animationEvent = _merge(animationEvent, {
          pitchCount: stringifyAtBat(eventPBP.count__list),
          outcome: sportConst.pitchOutcomes[eventPBP.outcome__id] || null,
          usedFlags: _filter(eventPBP.flags__list, flag => flag === 'true'),
          zonePitches: consolidateZonePitches(eventCall.zone_pitches),
        });

        // store multipart event for each player
        store.dispatch(storeEventMultipart(eventPBP.at_bat__id, animationEvent, relevantPlayersInEvent));

        // immediately update player stats, no need to wait bc there's no animation
        updatePBPPlayersStats(eventCall.stats);

        // TODO actions.events - what do we want to show in history?
        // store.dispatch(unshiftPlayerHistory(playerId, eventDescription));

      // otherwise just add animation event as per usual to show then hide
      } else {
        store.dispatch(addAnimationEvent(animationEvent.id, animationEvent));
      }

      break;
    case 'nba':
    default:
      animationEvent = {
        eventPBP,
        gameId: eventPBP.game__id,
        id: eventPBP.id,
        location: eventPBP.location__list,
        playersStats: eventCall.stats || null,
        relevantPlayersInEvent,
        whichSide: whichSide(watching, relevantPlayersInEvent, opponentLineup, relevantGamesPlayers),
      };
      store.dispatch(addAnimationEvent(animationEvent.id, animationEvent));
      store.dispatch(unionPlayersPlaying(relevantPlayersInEvent));

      break;
  }
};

/*
 * This takes the oldest event in a given game queue, from state.gamesQueue, and then uses the data, whether it is to
 * animate if a pbp, or update redux stats.
 *
 * @param  {string} gameId The game queue SRID to pop the oldest event
 */
export const shiftOldestGameEvent = (gameId) => {
  const state = store.getState();
  const gameQueue = _merge({}, state.events.gamesQueue[gameId]);

  // if there are no more events, then stop running
  if (gameQueue.queue.length === 0) {
    return;
  }

  // get oldest event
  const oldestEvent = gameQueue.queue.shift();
  const eventCall = oldestEvent.eventCall;

  // remove oldest event from redux
  store.dispatch(shiftGameQueueEvent(gameId));

  log.info(`actions.events.shiftOldestGameEvent(), game ${gameId}`, eventCall);

  // depending on what type of data, either show animation on screen or update stats
  switch (oldestEvent.type) {

    // if this is a court animation, then start er up
    case 'pbp':
      showGameEvent(eventCall, state, oldestEvent.sport);
      break;

    // if boxscore game, then update the clock/quarter
    case 'boxscore-game':
      log.info('Live.shiftOldestGameEvent().updateGameTime()', eventCall);

      store.dispatch(updateGameTime(
        eventCall.id,
        eventCall
      ));

      // then move on to the next
      shiftOldestGameEvent(gameId);
      break;

    // if boxscore team, then update the team points
    case 'boxscore-team':
      log.info('Live.shiftOldestGameEvent().updateGameTeam()', eventCall);

      store.dispatch(updateGameTeam(
        eventCall.game__id,
        eventCall.id,
        eventCall.points
      ));

      // then move on to the next
      shiftOldestGameEvent(gameId);
      break;

    // if stats, then update the player stats
    case 'stats': {
      const myLineup = watchingMyLineupSelector(state);
      const watching = state.watching;

      // don't update if we aren't ready
      if (watching.myLineupId === null || myLineup.isLoading === true) return false;

      log.info('Live.shiftOldestGameEvent().updatePlayerStats()', eventCall.fields.player_id);

      store.dispatch(updatePlayerStats(
        eventCall.fields.player_id,
        eventCall,
        myLineup.draftGroupId
      ));

      // then move on to the next
      shiftOldestGameEvent(gameId);
      break;
    }

    // no default
    default:
      break;
  }
};

/*
 * Helper method to add a new Pusher event to the appropriate state.[gameId] queue and then start the queue up
 *
 * @param {integer} gameId Game SRID to determine game queue
 * @param {object} event The json object received from Pusher
 * @param {string} type The type of call, options are 'stats', 'php', 'boxscore'
 * @param {string} sport [OPTIONAL] For PBP, pass through sport to know how to parse
 */
export const addEventAndStartQueue = (gameId, eventCall, type, sport) => {
  log.debug('actions.events.addEventAndStartQueue', gameId, eventCall, type, sport);

  store.dispatch(storeEvent(gameId, {
    eventCall,
    sport,
    type,
  }));
  shiftOldestGameEvent(gameId);
};
