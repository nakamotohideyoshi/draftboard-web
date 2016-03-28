import * as ActionTypes from '../action-types';
import log from '../lib/logging';
import store from '../store';
import { forEach as _forEach } from 'lodash';
import { intersection as _intersection } from 'lodash';
import { liveSelector } from '../selectors/live';
import { map as _map } from 'lodash';
import { merge as _merge } from 'lodash';
import { updateGameTeam } from './sports';
import { updateGameTime } from './sports';
import { updatePlayerStats } from './live-draft-groups';

const addAnimationEvent = (key, value) => ({
  type: ActionTypes.PUSHER_ADD_ANIMATION_EVENT,
  key,
  value,
});

const addPlayerEventDescription = (key, value) => ({
  type: ActionTypes.PUSHER_ADD_PLAYER_EVENT_DESCRIPTION,
  key,
  value,
});

const differencePlayersPlaying = (players) => ({
  type: ActionTypes.PUSHER_DIFFERENCE_PLAYERS_PLAYING,
  players,
});

const unionPlayersPlaying = (players) => ({
  type: ActionTypes.PUSHER_DIFFERENCE_PLAYERS_PLAYING,
  players,
});

export const removeAnimationEvent = (key) => ({
  type: ActionTypes.PUSHER_REMOVE_ANIMATION_EVENT,
  key,
});

const removePlayerEventDescription = (key) => ({
  type: ActionTypes.PUSHER_REMOVE_PLAYER_EVENT_DESCRIPTION,
  key,
});

const unshiftPlayerHistory = (key, value) => ({
  type: ActionTypes.PUSHER_UNSHIFT_PLAYER_HISTORY,
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
 * Dispatch information to reducer that we have completed getting all information related to the entries
 * Used to make the components aware tht we have finished pulling information.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
const addToGameQueue = (gameId, eventCall, type) => ({
  type: ActionTypes.PUSHER_ADD_GAME_QUEUE_EVENT,
  gameId,
  gameQueueEvent: {
    type,
    eventCall,
  },
});

/**
 * Dispatch information to reducer that we have completed getting all information related to the entries
 * Used to make the components aware tht we have finished pulling information.
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
export const shiftGameQueueEvent = (gameId) => ({
  gameId,
  type: ActionTypes.PUSHER_SHIFT_GAME_QUEUE_EVENT,
});

const whichSide = (relevantPlayersInEvent, liveSelectorData) => {
  // determine what color the animation should be, based on which lineup(s) the player(s) are in
  if (liveSelectorData.mode.opponentLineupId) {
    const rosterBySRID = liveSelectorData.lineups.opponent.rosterBySRID;
    const playersInBothLineups = liveSelectorData.playersInBothLineups;

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
  if (animationEvent.playersStats !== null) {
    const state = store.getState();
    const liveSelectorData = liveSelector(state);
    const players = liveSelectorData.draftGroup.playersInfo;

    _forEach(animationEvent.playersStats, (playerStats) => {
      const player = players[playerStats.fields.srid_player] || {};

      log.info('setTimeout - linked pbp - updatePlayerStats()', player.name || 'Unknown', animationEvent);

      store.dispatch(updatePlayerStats(
        playerStats.fields.player_id,
        playerStats,
        liveSelectorData.lineups.mine.draftGroup.id
      ));
    });
  }
};

/*
 * Show a game event from a Pusher pbp call in the court and in the player information
 * @param  {object} eventCall The event call to parse for information
 */
const showGameEvent = (eventCall, state) => {
  // get just pbp data if linked
  const eventPBP = eventCall.pbp || eventCall;

  const liveSelectorData = liveSelector(state);
  const eventPlayers = _map(eventPBP.statistics__list, event => event.player);
  const relevantPlayersInEvent = _intersection(liveSelectorData.relevantPlayers, eventPlayers);

  // relevant information for court animation
  const animationEvent = {
    eventPBP,
    gameId: eventPBP.game__id,
    id: eventPBP.id,
    location: eventPBP.location__list,
    playersStats: eventCall.stats || null,
    relevantPlayersInEvent,
    whichSide: whichSide(relevantPlayersInEvent, liveSelectorData),
  };

  store.dispatch(addAnimationEvent(animationEvent.id, animationEvent));
  store.dispatch(unionPlayersPlaying(relevantPlayersInEvent));
};

/*
 * This takes the oldest event in a given game queue, from state.gameQueues, and then uses the data, whether it is to
 * animate if a pbp, or update redux stats.
 *
 * @param  {string} gameId The game queue SRID to pop the oldest event
 */
export const shiftOldestGameEvent = (gameId) => {
  const state = store.getState();
  const gameQueue = _merge({}, state.pusherLive.gamesQueue[gameId]);

  // if there are no more events, then stop running
  if (gameQueue.queue.length === 0) {
    return;
  }

  // get oldest event
  const oldestEvent = gameQueue.queue.shift();
  const eventCall = oldestEvent.eventCall;

  // remove oldest event from redux
  store.dispatch(shiftGameQueueEvent(gameId));

  log.info(`actions.pusherLive.shiftOldestGameEvent(), game ${gameId}, queue of ${gameQueue.queue.length}`, eventCall);

  // depending on what type of data, either show animation on screen or update stats
  switch (oldestEvent.type) {

    // if this is a court animation, then start er up
    case 'pbp':
      showGameEvent(eventCall, state);
      break;

    // if boxscore game, then update the clock/quarter
    case 'boxscore-game':
      log.info('Live.shiftOldestGameEvent().updateGameTime()', eventCall);

      store.dispatch(updateGameTime(
        eventCall.id,
        eventCall.clock,
        eventCall.quarter,
        eventCall.status
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
    case 'stats':
      const liveSelectorData = liveSelector(state);

      // TODO mod this to work with results
      if (liveSelectorData.hasOwnProperty('draftGroup')) {
        const players = liveSelectorData.draftGroup.playersInfo;
        const player = players[eventCall.fields.playerId] || {};

        log.info('Live.shiftOldestGameEvent().updatePlayerStats()', player.name || 'Unknown', eventCall);

        store.dispatch(updatePlayerStats(
          eventCall.fields.player_id,
          eventCall,
          liveSelectorData.lineups.mine.draftGroup.id
        ));
      }

      // then move on to the next
      shiftOldestGameEvent(gameId);
      break;

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
 */
export const addEventAndStartQueue = (gameId, eventCall, type) => {
  log.debug('actions.pusherLive.addEventAndStartQueue', gameId, eventCall, type);

  store.dispatch(addToGameQueue(gameId, eventCall, type));
  shiftOldestGameEvent(gameId);
};
