import * as ActionTypes from '../action-types';
import forEach from 'lodash/forEach';
import intersection from 'lodash/intersection';
import log from '../lib/logging';
import { dateNow } from '../lib/utils';
import merge from 'lodash/merge';
import { updateGameTeam, updateGameTime } from './sports';
import { updatePlayerStats } from './live-draft-groups';
import { updateLiveMode } from './watching';
import { sportsSelector } from '../selectors/sports';
import { pastEvents, isPastEvent } from '../selectors/events-history';
import { removeEventMultipart, storeEventMultipart } from './events-multipart';
import {
  relevantGamesPlayersSelector,
  watchingOpponentLineupSelector,
  watchingMyLineupSelector,
} from '../selectors/watching';

// get custom logger for actions
const logAction = log.getLogger('action');

const addEventToHistory = (value) => ({
  type: ActionTypes.EVENT_ADD_TO_HISTORY,
  value,
});

const removePlayersPlaying = (players) => ({
  type: ActionTypes.EVENT_REMOVE_PLAYERS_PLAYING,
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

const setCurrentEvent = (value) => ({
  type: ActionTypes.EVENT__SET_CURRENT,
  value,
});

const clearCurrentEvent = () => ({
  type: ActionTypes.EVENT__REMOVE_CURRENT,
});

const unshiftPlayerHistory = (key, value) => ({
  type: ActionTypes.EVENT_UNSHIFT_PLAYER_HISTORY,
  key,
  value,
});

export const updatePBPPlayersStats = (sport, playersStats) => (dispatch) => {
  logAction.debug('actions.updatePBPPlayersStats', sport, playersStats);

  forEach(playersStats, (playerStats) => {
    dispatch(updatePlayerStats(sport, playerStats));
  });
};

/**
 * Returns the side representing all players provided.
 */
const whichSide = playersWithLineup => {
  const lineups = playersWithLineup.map(player => player.lineup);

  if (lineups.indexOf('mine') !== -1) {
    return 'mine';
  } else if (lineups.indexOf('opponent') !== -1) {
    return 'opponent';
  }

  return 'none';
};

/**
 * Returns an array of player SRIDs and their associated lineup ("mine",
 * "opponent", or "both").
 */
const whichSidePlayers = (players, state) => {
  const opponentLineup = watchingOpponentLineupSelector(state);
  const currentLineup = watchingMyLineupSelector(state);

  const isPlayerInLineup = (lineup, playerId) => {
    // A lot goes into making sure the lineup is loaded and contains all of
    // it's information so we're bailing if anything required is missing.
    if (!lineup || lineup.isLoading || !lineup.roster) {
      return false;
    }

    return lineup.roster.indexOf(playerId) !== -1;
  };

  return players.map(playerId => {
    const opponent = isPlayerInLineup(opponentLineup, playerId);
    const mine = isPlayerInLineup(currentLineup, playerId);
    let lineup = 'none';

    if (mine || opponent) {
      lineup = mine ? 'mine' : 'opponent';
    }

    // Add bypass for debugging whichside from live-animation-debugger.
    if (window.debug_live_animations_which_side) {
      lineup = window.debug_live_animations_which_side;
    }

    return { playerId, lineup };
  });
};

export const showAnimationEventResults = (animationEvent) => (dispatch) => {
  logAction.debug('actions.showAnimationEventResults', animationEvent);

  const { description, id, relevantPlayersInEvent, when } = animationEvent;

  const calls = [];
  const eventDescription = {
    description,
    id,
    points: null,
  };

  calls.push(dispatch(removePlayersPlaying(relevantPlayersInEvent)));

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
    case 'nba': {
      // show event beside player and in their history
      forEach(relevantPlayersInEvent, (playerId) => {
        const playerEventDescription = merge({}, eventDescription, { playerId });
        calls.push(dispatch(unshiftPlayerHistory(playerId, playerEventDescription)));
      });

      // update player stats if we have them
      calls.push(dispatch(updatePBPPlayersStats(animationEvent.sport, animationEvent.stats)));

      break;
    }
    case 'nfl': {
      eventDescription.when = when;

      // show event beside player and in their history
      forEach(relevantPlayersInEvent, (playerId) => {
        const playerEventDescription = merge({}, eventDescription, { playerId });
        calls.push(dispatch(unshiftPlayerHistory(playerId, playerEventDescription)));
      });

      // update player stats if we have them
      calls.push(dispatch(updatePBPPlayersStats(animationEvent.sport, animationEvent.stats)));
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
export const showGameEvent = (event) => (dispatch, getState) => {
  const state = getState();
  const watching = state.watching;
  const opponentLineup = watchingOpponentLineupSelector(state);
  const relevantGamesPlayers = relevantGamesPlayersSelector(state);
  const { playersStats, sport, message } = event;
  const eventPlayers = message.stats.map(stat => stat.srid_player);
  const relevantPlayersInEvent = intersection(relevantGamesPlayers.relevantItems.players, eventPlayers);
  const playersBySide = whichSidePlayers(message.stats.map(stat => stat.player_id), state);

  // Update message to reflect current lineups the user is watching
  const gameEvent = merge({}, message, {
    relevantPlayersInEvent,
    whichSide: whichSide(playersBySide),
    whichSidePlayers: playersBySide,
  });

  if (!window.is_debugging_live_animation) {
    // Skip animating PBPs that are already in event history.
    if (isPastEvent(pastEvents(state), gameEvent.id)) {
      return Promise.resolve();
    }

    // Skip animating PBPs that are more than 3 minutes (180000ms) old.
    if ((event.queuedAt + 1000) < dateNow()) {
      return Promise.resolve();
    }

    // Skip animating PBPs that are irrelevant to the current lineup.
    if (whichSide === 'none') {
      return Promise.resolve();
    }
  }

  if (sport === 'mlb') {
    // The following block of property assignments for `homeSCoreStr`, `awayScoreStr`
    // and `winning` is here because I'm not sure if MLB works the same way as
    // NFL or NBA, which get's it's game info as soon as the event is queued via
    // `addEventAndStartQueue`. Without this block, the tests fail at...
    // "should create promise of multievent and updating stats if valid mlb pbp with relevant player"
    const sports = sportsSelector(state);
    const game = sports.games[message.gameId];
    const homeScore = game.home_score;
    const awayScore = game.away_score;
    gameEvent.homeScoreStr = `${game.homeTeamInfo.alias} ${homeScore}`;
    gameEvent.awayScoreStr = `${game.awayTeamInfo.alias} ${awayScore}`;
    gameEvent.winning = (homeScore > awayScore) ? 'home' : 'away';

    // add in which side runners are on, for the mlb diamond
    gameEvent.runners = gameEvent.runners.map(
      (runner) => merge({}, runner, {
        whichSide: 'mine', // NFL/NBA logic has broken this... we'll need to re-implement during MLB.
      })
    );

    // after 5 seconds, remove the at bat from multipart-events
    if (message.isAtBatOver) {
      logAction.warn('At bat over for ', { info: { relevantPlayersInEvent, gameEvent } });
      setTimeout(() => dispatch(showAnimationEventResults(gameEvent)), 5000);
    }

    return Promise.all([
      dispatch(storeEventMultipart(message.sridAtBat, gameEvent, relevantPlayersInEvent)),
      dispatch(updatePBPPlayersStats(sport, playersStats)),
    ]);
  }

  return Promise.all([
    dispatch(setCurrentEvent(gameEvent)),
    dispatch(unionPlayersPlaying(relevantPlayersInEvent)),
  ]);
};

/*
 * This takes the oldest event in a given game queue, from state.queue, then
 * uses the data, whether it is to animate if a pbp, or update redux stats.
 */
export const shiftOldestEvent = () => (dispatch, getState) => {
  logAction.debug('actions.shiftOldestEvent');

  const state = getState();
  const queue = [...state.events.queue];

  // If an event is currently being processed do not shift a new in its place.
  if (state.events.currentEvent !== null) {
    return false;
  }

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
      return dispatch(showGameEvent(oldestEvent, state, oldestEvent.sport));
    case 'boxscore-game':
      dispatch(updateGameTime(message));
      break;
    case 'boxscore-team':
      dispatch(updateGameTeam(message));
      break;
    case 'stats': {
      dispatch(updatePlayerStats(oldestEvent.sport, message));
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
    dispatch(pushEvent({ message, sport, type, queuedAt: dateNow() })),
  ]).then(
    () => dispatch(shiftOldestEvent())
  );
};

/**
 * Clears the current animation event, if it exists. Clearing the event includes
 * showing the "results" of the animation, which would include things like
 * updating player history, stats, and FP.
 */
export const clearCurrentAnimationEvent = () => (dispatch, getState) => {
  logAction.debug('actions.clearCurrentAnimationEvent');

  const { currentEvent } = getState().events;

  if (!currentEvent) {
    return Promise.resolve();
  }

  return Promise.resolve()
  .then(() => dispatch(addEventToHistory(currentEvent)))          // Push to history
  .then(() => dispatch(showAnimationEventResults(currentEvent)))  // Update FP and stats.
  .then(() => dispatch(clearCurrentEvent()))                      // Remove current event
  .then(() => dispatch(shiftOldestEvent()));                      // Bring in the next one
};
