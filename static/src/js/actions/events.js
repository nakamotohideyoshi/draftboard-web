import * as ActionTypes from '../action-types';
import forEach from 'lodash/forEach';
import intersection from 'lodash/intersection';
import log from '../lib/logging';
import merge from 'lodash/merge';
import { updateGameTeam, updateGameTime } from './sports';
import { updatePlayerStats } from './live-draft-groups';
import { updateLiveMode } from './watching';
import { sportsSelector } from '../selectors/sports';
import { removeEventMultipart, storeEventMultipart } from './events-multipart';
import {
  relevantGamesPlayersSelector,
  watchingOpponentLineupSelector,
  watchingMyLineupSelector,
} from '../selectors/watching';

// get custom logger for actions
const logAction = log.getLogger('action');

const addEventToBigPlays = (value) => ({
  type: ActionTypes.EVENT_ADD_TO_BIG_QUEUE,
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
const whichSide = playersWithLineup => (
  playersWithLineup.reduce((side, player) => {
    if (side === 'none') {
      return player.lineup;
    }
    const isMixed = side !== player.lineup || side === 'both';
    return isMixed ? 'both' : player.lineup;
  }, 'none')
);

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
      lineup = mine ? 'mine' : 'oppponent';
    }

    return { playerId, lineup };
  });
};

/**
 * Returns an object of player names keyed by their matching Sports Radar IDs.
 */
const getPlayerNames = (srIds, draftGroup) => {
  const names = srIds.map((srid) => {
    for (const playerId in draftGroup.playersInfo) {
      if (Object.prototype.hasOwnProperty.call(draftGroup.playersInfo, playerId)) {
        const player = draftGroup.playersInfo[playerId];
        if (player.player_srid === srid) {
          return {
            player_srid: player.player_srid,
            name: player.name,
          };
        }
      }
    }
    return null;
  });

  // Filter all `NULL` values and convert from an array to an object keyed by
  // the player's associated Sports Radar ID.
  return names.filter(player => player !== null).reduce((obj, playerInfo) => {
    const objWithPlayer = obj;
    objWithPlayer[playerInfo.player_srid] = playerInfo.name;
    return obj;
  }, {});
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

  // add to big plays, if relevant
  if (relevantPlayersInEvent.length > 0 || animationEvent.isBigPlay || window.is_debugging_live_animation) {
    calls.push(dispatch(addEventToBigPlays(animationEvent)));
  }

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
export const showGameEvent = (message) => (dispatch, getState) => {
  logAction.debug('actions.showGameEvent', message);

  // selectors
  const state = getState();
  const watching = state.watching;
  const opponentLineup = watchingOpponentLineupSelector(state);
  const relevantGamesPlayers = relevantGamesPlayersSelector(state);

  const { eventPlayers, playersStats, sport } = message;
  const relevantPlayersInEvent = intersection(relevantGamesPlayers.relevantItems.players, eventPlayers);

  // if there are no more relevant players, just update stats
  if (relevantPlayersInEvent.length === 0 && !window.is_debugging_live_animation) {
    const calls = [];
    calls.push(dispatch(updatePBPPlayersStats(sport, playersStats)));
    return Promise.all(calls);
  }

  // Return an object containing the names of all known players in the PBP.
  let names = {};
  if (watching.myLineupId !== null) {
    const currentLineup = state.currentLineups.items[watching.myLineupId];
    const draftGroup = state.liveDraftGroups[currentLineup.draftGroup];
    names = getPlayerNames(eventPlayers, draftGroup);
  }

  const playersBySide = whichSidePlayers(message.stats.map(stat => stat.player_id), state);

  // update message to reflect current lineups the user is watching
  const animationEvent = merge({}, message, {
    playerNames: names,
    relevantPlayersInEvent,
    whichSide: whichSide(playersBySide),
    whichSidePlayers: playersBySide,
  });

  // Remap the whichSide flags based on our debugging settings.
  if (window.debug_live_animations_which_side) {
    animationEvent.whichSide = window.debug_live_animations_which_side;
    animationEvent.whichSidePlayers = animationEvent.whichSidePlayers.map(player => {
      /* eslint-disable */
      player.lineup = animationEvent.whichSide
      /* eslint-enable */
      return player;
    });
  }

  switch (sport) {
    case 'mlb': {
      // The following block of property assignments for `homeSCoreStr`, `awayScoreStr`
      // and `winning` is here because I'm not sure if MLB works the same way as
      // NFL or NBA, which get's it's game info as soon as the event is queued via
      // `addEventAndStartQueue`. Without this block, the tests fail at...
      // "should create promise of multievent and updating stats if valid mlb pbp with relevant player"
      const sports = sportsSelector(state);
      const game = sports.games[message.gameId];
      const homeScore = game.home_score;
      const awayScore = game.away_score;
      animationEvent.homeScoreStr = `${game.homeTeamInfo.alias} ${homeScore}`;
      animationEvent.awayScoreStr = `${game.awayTeamInfo.alias} ${awayScore}`;
      animationEvent.winning = (homeScore > awayScore) ? 'home' : 'away';

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
        dispatch(updatePBPPlayersStats(sport, playersStats)),
      ]);
    }

    case 'nba':
    case 'nfl':
      return Promise.all([
        dispatch(setCurrentEvent(animationEvent)),
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
      return dispatch(showGameEvent(message, state, oldestEvent.sport));
    case 'boxscore-game':
      dispatch(updateGameTime(message));
      break;
    case 'boxscore-team':
      dispatch(updateGameTeam(message));
      break;
    case 'stats': {
      // TODO: This has to be dispatched as a validation check of some sort!
      // dispatch(updatePlayerStats(oldestEvent.sport, message));
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
    dispatch(pushEvent({ message, sport, type })),
  ]).then(
    () => dispatch(shiftOldestEvent(gameId))
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
  .then(() => dispatch(showAnimationEventResults(currentEvent)))  // Update bigplays, FP, and stats.
  .then(() => dispatch(clearCurrentEvent()))                      // Remove current event
  .then(() => dispatch(shiftOldestEvent()));                      // Bring in the next one
};
