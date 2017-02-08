import log from '../../lib/logging';
import { addEventAndStartQueue } from '../events';
import { isGameReady } from '../sports';

// get custom logger for actions
const logAction = log.getLogger('action');

/**
 * Figure out sport by message content
 * @param  {object} games   List of games, key is ID
 * @param  {string} gameId  SportsRadar UUID
 * @return {mixed}          Sport || false
 */
const calcSportByGame = (games = {}, gameId) => {
  logAction.debug('actions.calcSportByGame', gameId);

  if (!(gameId in games)) return false;
  return games[gameId].sport || false;
};

/**
 * Check whether we would even want to use this PBP
 * @param  {object} message Pusher event message
 * @param  {string} sport   Sport, based on available actions.sport.SPORT_CONST
 * @return {boolean}        True if we want to use, false if we don't
 */
const isMessageUsed = (message, sport) => {
  logAction.trace('actions.isMessageUsed');

  const reasons = [];

  // check that game is relevant
  if (message.status === 'scheduled') reasons.push('message.status is scheduled');

  switch (sport) {
    case 'mlb':
      // check that we have data to work with
      if (message.status === 'inprogress' && !('outcome__list' in message)) reasons.push('!message.outcome__list');
      if (['complete', 'closed'].indexOf(message.status) > -1 && !('final__list' in message)) {
        reasons.push('!message.final__list');
      }
      break;
    case 'nba':
    case 'nfl':
      if (message.status === 'inprogress' && (!('clock' in message) || !('quarter' in message))) {
        reasons.push('!message.outcome__list');
      }
      break;
    default:
      break;
  }

  // returns false
  if (reasons.length > 0) return false;

  return true;
};

/*
 * Take a pusher call, validate, then reshape to fit into store.events
 * `boxscore.game` message depends on sport:
 * - MLB docs here https://git.io/vofys
 * - NBA docs here https://git.io/vofyz
 *
 * @param  {object} message The received event from Pusher
 */
export const onBoxscoreGameReceived = (message) => (dispatch, getState) => {
  logAction.debug('actions.onBoxscoreGameReceived', message);

  const gameId = message.srid_game;
  const state = getState();

  const sport = calcSportByGame(state.sports.games, gameId);
  if (!sport) return false;

  if (!isMessageUsed(message, sport)) return false;

  const status = message.status;
  const updatedFields = {
    status,
  };

  switch (sport) {
    case 'mlb': {
      switch (status) {
        case 'inprogress': {
          const latestList = message.outcome__list;

          updatedFields.boxscore = {
            inning: latestList.current_inning,
            inning_half: latestList.current_inning_half,
          };
          break;
        }
        case 'complete':
        case 'closed':
        default: {
          const latestList = message.final__list;

          updatedFields.boxscore = {
            inning: latestList.inning,
            inning_half: latestList.inning_half,
          };
          break;
        }
      }
      break;
    }
    case 'nba':
    case 'nfl': {
      updatedFields.boxscore = message;
      break;
    }
    default:
      break;
  }

  const relevantData = {
    gameId,
    updatedFields,
  };

  return dispatch(addEventAndStartQueue(gameId, relevantData, 'boxscore-game', sport));
};

/*
 * Take a pusher call, validate, then reshape to fit into store.events
 * `boxscore.team` message depends on sport:
 * - NBA docs here https://git.io/vofyK
 *
 * @param  {object} message The received event from Pusher
 */
export const onBoxscoreTeamReceived = (message) => (dispatch, getState) => {
  logAction.debug('actions.onBoxscoreTeamReceived', message);
  const gameId = message.srid_game;
  const state = getState();
  const sport = calcSportByGame(state.sports.games, gameId);

  if (!sport) {
    log.warn(`no sport exists for this gameId: ${gameId}`);
    return false;
  }

  if (!isGameReady(state, dispatch, sport, gameId)) {
    log.warn('game not ready');
    return false;
  }

  return dispatch(addEventAndStartQueue(gameId, message, 'boxscore-team', sport));
};
