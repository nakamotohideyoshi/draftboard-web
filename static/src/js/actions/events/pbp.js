import intersection from 'lodash/intersection';
import map from 'lodash/map';
import merge from 'lodash/merge';

import { addEventAndStartQueue, updatePBPPlayersStats } from '../events';
import { isGameReady } from '../sports';


/**
 * Parse the message content for any players involved
 * @param  {object} message Pusher event message
 * @param  {string} sport   Sport, based on available actions.sport.SPORT_CONST
 * @return {array}          List of players
 */
const compileEventPlayers = (message, sport) => {
  switch (sport) {
    case 'mlb': {
      const eventPlayers = [
        message.pbp.pitcher,  // pitcher
        message.at_bat_stats.id,  // hitter
      ];

      // runners on base
      if (message.hasOwnProperty('runners')) {
        message.runners.map((runner) => eventPlayers.push(runner.id));
      }

      return eventPlayers;
    }
    case 'nba':
      return map(message.statistics__list, event => event.player);
    default:
      return [];
  }
};

/**
 * Check whether we would even want to use this PBP
 * @param  {object} message Pusher event message
 * @param  {string} sport   Sport, based on available actions.sport.SPORT_CONST
 * @return {boolean}        True if we want to use, false if we don't
 */
const isMessageUsed = (message, sport) => {
  switch (sport) {
    case 'mlb':
      // TODO fix backend, call came in with null at_bat_stats
      if (!message.at_bat_stats || !message.at_bat_stats.hasOwnProperty('id')) return false;
      break;
    case 'nba':
      if (!message.pbp.hasOwnProperty('statistics__list')) return false;
      if (!message.pbp.hasOwnProperty('location__list')) return false;
      break;
    default:
      return false;
  }

  return true;
};

/*
 * Take a pusher call, validate, then reshape to fit into store.events
 * `message` depends on sport:
 * - MLB `mlb_pbp.linked` docs here https://git.io/vofyM
 * - MLB `mlb_pbp.event` docs here https://git.io/vofyD
 * - NBA `nba_pbp.linked` docs here https://git.io/vofyy
 *
 * @param  {object} message The received event from Pusher
 */
export const onPBPReceived = (message, sport, relevantPlayers) => (dispatch, getState) => {
  const pbp = message.pbp;
  const gameId = pbp.game__id;

  if (!isGameReady(getState(), dispatch, sport, gameId)) return false;
  if (!isMessageUsed(message, sport)) return false;

  const eventPlayers = compileEventPlayers(message, sport);
  if (intersection(relevantPlayers, eventPlayers).length === 0) {
    return dispatch(updatePBPPlayersStats(message.stats));
  }

  const loadedMessage = merge(message, {
    addedData: {
      eventPlayers,
      sport,
    },
  });

  return dispatch(addEventAndStartQueue(gameId, loadedMessage, 'pbp', sport));
};

/*
 * Shortcut method to pull events into linked, as it's a subset of linked anyways
 */
export const onPBPEventReceived = (message, sport, relevantPlayers) => (dispatch) => {
  const linkedMessage = {
    pbp: message,
  };

  return dispatch(onPBPReceived(linkedMessage, sport, relevantPlayers));
};
