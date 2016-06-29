import log from '../../lib/logging';
import { addEventAndStartQueue } from '../events';
import { hasGameStarted, isGameReady } from '../sports';

/**
 * Figure out sport by message content
 * @param  {object} message Socket message received
 * @return {mixed}          Sport || false
 */
const calcBoxscoreGameSport = (message) => {
  if (message.hasOwnProperty('clock')) return 'nba';
  if (message.hasOwnProperty('outcome__list')) return 'mlb';
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

/*
 * Take a pusher call, validate, then reshape to fit into store.events
 * `boxscore.game` message depends on sport:
 * - MLB docs here https://git.io/vofys
 * - NBA docs here https://git.io/vofyz
 *
 * @param  {object} message The received event from Pusher
 */
export const onBoxscoreGameReceived = (message) => (dispatch, getState) => {
  log.trace('onBoxscoreGameReceived', message);
  const gameId = message.id;

  const sport = calcBoxscoreGameSport(message);
  if (!sport) return false;


  if (!isGameReady(getState(), dispatch, sport, gameId)) return false;
  if (!hasGameStarted(sport, message.status)) return false;

  return dispatch(addEventAndStartQueue(gameId, message, 'boxscore-game', sport));
};

/*
 * Take a pusher call, validate, then reshape to fit into store.events
 * `boxscore.team` message depends on sport:
 * - NBA docs here https://git.io/vofyK
 *
 * @param  {object} message The received event from Pusher
 */
export const onBoxscoreTeamReceived = (message) => (dispatch, getState) => {
  log.trace('onBoxscoreTeamReceived', message);
  const gameId = message.game__id;

  const sport = calcBoxscoreTeamSport(message);
  if (!sport) return false;

  if (!isGameReady(getState(), dispatch, sport, gameId)) return false;

  return dispatch(addEventAndStartQueue(gameId, message, 'boxscore-team', sport));
};
