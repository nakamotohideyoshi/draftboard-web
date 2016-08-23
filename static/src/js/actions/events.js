import * as ActionTypes from '../action-types';
import forEach from 'lodash/forEach';
import intersection from 'lodash/intersection';
import log from '../lib/logging';
import merge from 'lodash/merge';
import { updateGameTeam, updateGameTime } from './sports';
import { updatePlayerStats } from './live-draft-groups';
import { updateLiveMode } from './watching';
import {
  removeEventMultipart,
  storeEventMultipart,
} from './events-multipart';
import {
  relevantGamesPlayersSelector,
  watchingMyLineupSelector,
  watchingOpponentLineupSelector,
} from '../selectors/watching';

// get custom logger for actions
const logAction = log.getLogger('action');


const setCurrentAnimation = (value) => ({
  type: ActionTypes.EVENT__SET_CURRENT,
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

const pushEvent = (event) => ({
  type: ActionTypes.EVENT_GAME_QUEUE_PUSH,
  event,
});

const shiftEvent = () => ({
  type: ActionTypes.EVENT_SHIFT_GAME_QUEUE,
});

/**
 * Action creator for removing an event
 * NOTE: exported because nba calls this after animation
 * @param  {string} key SportsRadar UUID for event
 * @return {object}     Object that, when combined with `dispatch()`, updates reducer
 */
export const removeCurrentEvent = (key) => ({
  type: ActionTypes.EVENT__REMOVE_CURRENT,
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
  logAction.debug('actions.updatePBPPlayersStats');

  const state = getState();
  const myLineup = watchingMyLineupSelector(state);
  const { draftGroupId } = myLineup;

  // if there's nowhere to put the data, don't bother
  if (!state.liveDraftGroups[draftGroupId]) return false;
  if (!state.liveDraftGroups[draftGroupId].playersStats) return false;

  forEach(playersStats, (playerStats) => {
    const playerId = playerStats.fields.player_id;
    if (state.liveDraftGroups[draftGroupId].playersStats.hasOwnProperty(playerId)) {
      dispatch(updatePlayerStats(playerStats, draftGroupId));
    }
  });
};

const whichSide = (watching, relevantPlayersInEvent, opponentLineup, relevantGamesPlayers) => {
  logAction.debug('actions.whichSide');

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

const showThenHidePlayerEventDescription = (key, value) => (dispatch) => {
  logAction.debug('actions.showThenHidePlayerEventDescription');

  dispatch(addPlayerEventDescription(key, value));

  setTimeout(() => {
    dispatch(removePlayerEventDescription(key));
  }, 3000);
};

export const showAnimationEventResults = (animationEvent) => (dispatch) => {
  logAction.debug('actions.showAnimationEventResults');

  const { description, id, relevantPlayersInEvent, when } = animationEvent;

  const calls = [];
  const eventDescription = {
    description,
    id,
    points: null,
  };

  calls.push(dispatch(differencePlayersPlaying(relevantPlayersInEvent)));

  switch (animationEvent.sport) {
    case 'mlb': {
      const { sridAtBat } = animationEvent;

      calls.push(dispatch(updateLiveMode({
        myPlayerSRID: null,
        opponentPlayerSRID: null,
      })));

      eventDescription.when = when.humanized;

      // show event beside player and in their history
      forEach(relevantPlayersInEvent, (playerId) => {
        const playerEventDescription = merge({}, eventDescription, { playerId });
        calls.push(dispatch(unshiftPlayerHistory(playerId, playerEventDescription)));
      });

      calls.push(dispatch(removeEventMultipart(sridAtBat, relevantPlayersInEvent)));

      break;
    }
    case 'nba':
    case 'nfl': {
      eventDescription.when = when;

      // show event beside player and in their history
      forEach(relevantPlayersInEvent, (playerId) => {
        const playerEventDescription = merge({}, eventDescription, { playerId });

        calls.push(dispatch(unshiftPlayerHistory(playerId, playerEventDescription)));
        calls.push(dispatch(showThenHidePlayerEventDescription(playerId, playerEventDescription)));
      });

      // update player stats if we have them
      calls.push(dispatch(updatePBPPlayersStats(animationEvent.playersStats)));

      break;
    }
    default:
      return Promise.reject('Improper sport when showing event results');
  }

  return Promise.all(calls);
};

/*
 * Show a game event from a Pusher pbp call. If this is a multipart, then add there, otherwise just add as normal event
 * Is exported bc we need to test, too big
 * @param  {object} message The event call to parse for information
 */
export const showGameEvent = (message) => (dispatch, getState) => {
  logAction.debug('actions.showGameEvent');

  // selectors
  const state = getState();
  const watching = state.watching;
  const opponentLineup = watchingOpponentLineupSelector(state);
  const relevantGamesPlayers = relevantGamesPlayersSelector(state);

  const { eventPlayers, playersStats, sport } = message;
  const relevantPlayersInEvent = intersection(relevantGamesPlayers.relevantItems.players, eventPlayers);

  // if there are no more relevant players, just update stats
  if (relevantPlayersInEvent.length === 0) return dispatch(updatePBPPlayersStats(playersStats));

  logAction.debug('showGameEvent has relevant player(s)', relevantPlayersInEvent);

  // update message to reflect current lineups the user is watching
  const animationEvent = merge({}, message, {
    relevantPlayersInEvent,
    whichSide: whichSide(watching, relevantPlayersInEvent, opponentLineup, relevantGamesPlayers),
  });

  switch (sport) {
    case 'mlb': {
      // add in which side runners are on, for the mlb diamond
      animationEvent.runners = animationEvent.runners.map(
        (runner) => merge({}, runner, {
          whichSide: whichSide(watching, [runner.id], opponentLineup, relevantGamesPlayers),
        })
      );

      // after 5 seconds, remove the at bat from multipart-events
      if (message.isAtBatOver) {
        logAction.warn('At bat over for ', { info: { relevantPlayersInEvent, animationEvent } });
        setTimeout(() => dispatch(showAnimationEventResults(animationEvent)), 5000);
      }

      return Promise.all([
        dispatch(storeEventMultipart(message.sridAtBat, animationEvent, relevantPlayersInEvent)),
        dispatch(updatePBPPlayersStats(playersStats)),
      ]);
    }

    case 'nba':
    case 'nfl':
      return Promise.all([
        dispatch(setCurrentAnimation(animationEvent)),
        dispatch(unionPlayersPlaying(relevantPlayersInEvent)),
      ]);

    default:
      return Promise.reject('Improper sport when showing event');
  }
};

/*
 * This takes the oldest event in a given game queue, from state.queue, and then uses the data, whether it is to
 * animate if a pbp, or update redux stats.
 *
 * @param  {string} gameId The game queue SRID to pop the oldest event
 */
export const shiftOldestEvent = () => (dispatch, getState) => {
  logAction.debug('actions.shiftOldestEvent');

  const state = getState();
  const queue = [...state.events.queue];

  // if there are no more events, then stop running
  if (queue.length === 0) {
    logAction.debug('actions.shiftOldestEvent - queue empty');
    return false;
  }

  // get and remove oldest event
  const oldestEvent = queue.shift();
  const { message, type } = oldestEvent;
  dispatch(shiftEvent());

  switch (type) {
    case 'pbp':
      return dispatch(showGameEvent(message, state, oldestEvent.sport));
    case 'boxscore-game':
      dispatch(updateGameTime(message));
      break;
    case 'boxscore-team':
      dispatch(updateGameTeam(message));
      break;
    case 'stats': {
      const myLineup = watchingMyLineupSelector(state);
      dispatch(updatePlayerStats(message, myLineup.draftGroupId));
      break;
    }
    default:
      break;
  }

  // this runs for any option other than pbp, which already returned
  // this is bc of the animations that get run with pbp
  return dispatch(shiftOldestEvent());
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
  logAction.debug('actions.events.addEventAndStartQueue', gameId, message, type, sport);

  return Promise.all([
    dispatch(pushEvent({
      message,
      sport,
      type,
    })),
  ]).then(
    () => dispatch(shiftOldestEvent(gameId))
  );
};
