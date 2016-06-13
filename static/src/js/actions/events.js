import * as ActionTypes from '../action-types';
import filter from 'lodash/filter';
import forEach from 'lodash/forEach';
import intersection from 'lodash/intersection';
import log from '../lib/logging';
import merge from 'lodash/merge';
import store from '../store';
import { batchActions } from 'redux-batched-actions';
import { SPORT_CONST, updateGameTeam, updateGameTime } from './sports';
import { updatePlayerStats } from './live-draft-groups';
import {
  consolidateZonePitches,
  removeEventMultipart,
  storeEventMultipart,
  stringifyAtBat,
  stringifyMLBWhen,
} from './events-multipart';
import {
  relevantGamesPlayersSelector,
  watchingMyLineupSelector,
  watchingOpponentLineupSelector,
} from '../selectors/watching';


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

/**
 * Action creator for removing an event
 * NOTE: exported because nba calls this after animation
 * @param  {string} key SportsRadar UUID for event
 * @return {object}     Object that, when combined with `dispatch()`, updates reducer
 */
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

export const updatePBPPlayersStats = (playersStats) => (dispatch, getState) => {
  const state = getState();
  const myLineup = watchingMyLineupSelector(state);
  const { draftGroupId } = myLineup;

  if (!state.liveDraftGroups[draftGroupId]) return false;

  forEach(playersStats, (playerStats) => {
    const playerId = playerStats.fields.player_id;
    log.info('updatePBPPlayersStats - linked pbp - updatePlayerStats()', playerId);

    if (state.liveDraftGroups[draftGroupId].playersStats.hasOwnProperty(playerId)) {
      dispatch(updatePlayerStats(playerStats, draftGroupId));
    }
  });
};

const whichSide = (watching, relevantPlayersInEvent, opponentLineup, relevantGamesPlayers) => {
  // determine what color the animation should be, based on which lineup(s) the player(s) are in
  if (watching.opponentLineupId && opponentLineup.isLoading === false) {
    const rosterBySRID = opponentLineup.rosterBySRID;
    const playersInBothLineups = relevantGamesPlayers.playersInBothLineups;

    if (intersection(rosterBySRID, relevantPlayersInEvent).length > 0) {
      return 'opponent';
    }
    if (intersection(playersInBothLineups, relevantPlayersInEvent).length > 0) {
      return 'both';
    }
  }

  return 'mine';
};

/*
 * Show a game event from a Pusher pbp call. If this is a multipart, then add there, otherwise just add as normal event
 * @param  {object} message The event call to parse for information
 */
const showGameEvent = (message, state) => {
  log.trace('showGameEvent', message, state);

  // get just pbp data if linked
  const eventPBP = message.pbp || message;

  const opponentLineup = watchingOpponentLineupSelector(state);
  const relevantGamesPlayers = relevantGamesPlayersSelector(state);
  const watching = state.watching;
  const eventPlayers = message.addedData.eventPlayers;
  const relevantPlayersInEvent = intersection(relevantGamesPlayers.relevantItems.players, eventPlayers);
  const sport = message.addedData.sport;
  const sportConst = SPORT_CONST[sport];

  // relevant information for court animation
  let animationEvent;

  switch (sport) {
    case 'mlb':
      animationEvent = {
        eventPBP,
        message,
        gameId: eventPBP.game__id,
        id: eventPBP.id,
        playersStats: message.stats || {},
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
              forEach(animationEvent.relevantPlayersInEvent, (playerId) => {
                const eventDescription = {
                  points: null,
                  info: message.at_bat.description,
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

        animationEvent = merge(animationEvent, {
          pitchCount: stringifyAtBat(eventPBP.count__list),
          outcome: sportConst.pitchOutcomes[eventPBP.outcome__id] || null,
          usedFlags: filter(eventPBP.flags__list, flag => flag === 'true'),
          zonePitches: consolidateZonePitches(message.zone_pitches),
          runnerIds: message.runners.map(runner => runner.id),
          runners: message.runners.map((runner) => ({
            whichSide: whichSide(watching, [runner.id], opponentLineup, relevantGamesPlayers),
            playerSrid: runner.id,
            endingBase: runner.ending_base,
          })),
        });

        // store multipart event for each player
        store.dispatch(storeEventMultipart(eventPBP.at_bat__id, animationEvent, relevantPlayersInEvent));

        // immediately update player stats, no need to wait bc there's no animation
        store.dispatch(updatePBPPlayersStats(message.stats));

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
        playersStats: message.stats || null,
        relevantPlayersInEvent,
        whichSide: whichSide(watching, relevantPlayersInEvent, opponentLineup, relevantGamesPlayers),
      };
      store.dispatch(addAnimationEvent(animationEvent.id, animationEvent));
      store.dispatch(unionPlayersPlaying(relevantPlayersInEvent));

      break;
  }
};

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

export const showAnimationEventResults = (animationEvent) => {
  log.debug('setTimeout - show the results');

  store.dispatch(differencePlayersPlaying(animationEvent.relevantPlayersInEvent));

  const eventPBP = animationEvent.eventPBP;

  // show event beside player and in their history
  forEach(animationEvent.relevantPlayersInEvent, (playerId) => {
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
 * This takes the oldest event in a given game queue, from state.gamesQueue, and then uses the data, whether it is to
 * animate if a pbp, or update redux stats.
 *
 * @param  {string} gameId The game queue SRID to pop the oldest event
 */
export const shiftOldestGameEvent = (gameId) => {
  const state = store.getState();
  const gameQueue = merge({}, state.events.gamesQueue[gameId]);

  // if there are no more events, then stop running
  if (!gameQueue.queue || gameQueue.queue.length === 0) return;

  // get and remove oldest event
  const oldestEvent = gameQueue.queue.shift();
  store.dispatch(shiftGameQueueEvent(gameId));

  const message = oldestEvent.message;

  switch (oldestEvent.type) {
    case 'pbp':
      showGameEvent(message, state, oldestEvent.sport);
      break;
    case 'boxscore-game':
      store.dispatch(updateGameTime(message));
      break;
    case 'boxscore-team':
      store.dispatch(updateGameTeam(message));
      break;
    case 'stats': {
      const myLineup = watchingMyLineupSelector(state);

      store.dispatch(updatePlayerStats(message, myLineup.draftGroupid));
      break;
    }
    default:
      return;
  }

  // move on to the next
  if (oldestEvent.type !== 'pbp') {
    shiftOldestGameEvent(gameId);
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
export const addEventAndStartQueue = (gameId, message, type, sport) => (dispatch) => {
  log.debug('actions.events.addEventAndStartQueue', gameId, message, type, sport);

  dispatch(storeEvent(gameId, {
    message,
    sport,
    type,
  }));
  shiftOldestGameEvent(gameId);
};
