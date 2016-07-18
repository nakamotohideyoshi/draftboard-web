import log from '../../lib/logging';
import { addEventAndStartQueue } from '../events';
import { hasGameStarted, isGameReady } from '../sports';
import { trackUnexpected } from '../track-exceptions';

// get custom logger for actions
const logAction = log.getLogger('action');

/**
 * Figure out sport by message content
 * @param  {object} message Socket message received
 * @return {mixed}          Sport || false
 */
const calcBoxscoreGameSport = (message) => {
  if (message.hasOwnProperty('clock')) return 'nba';
  if (message.hasOwnProperty('outcome__list') || message.hasOwnProperty('final__list')) return 'mlb';
  return false;
};

/**
 * Figure out sport by message content
 * @param  {object} message Socket message received
 * @return {mixed}          Sport || false
 */
const calcBoxscoreTeamSport = (message) => {
  if (message.hasOwnProperty('points')) return 'nba';
  return false;
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
    default:
      break;
  }

  // returns false
  if (reasons.length > 0) return trackUnexpected('boxscores.isMessageUsed returned false', { message, reasons });

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

  const gameId = message.id;

  const sport = calcBoxscoreGameSport(message);
  if (!sport) return false;

  if (!isGameReady(getState(), dispatch, sport, gameId)) return false;
  if (!hasGameStarted(sport, message.status)) return false;
  if (!isMessageUsed(message, sport)) return false;

  const updatedFields = {};

  switch (sport) {
    case 'mlb': {
      const status = message.status;
      updatedFields.status = status;

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
    case 'nba': {
      const status = message.status;
      updatedFields.status = status;

      updatedFields.boxscore = {
        clock: message.boxscore.clock,
        quarter: message.boxscore.quarter,
      };
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

  const gameId = message.game__id;

  const sport = calcBoxscoreTeamSport(message);
  if (!sport) return false;

  if (!isGameReady(getState(), dispatch, sport, gameId)) return false;

  return dispatch(addEventAndStartQueue(gameId, message, 'boxscore-team', sport));
};
