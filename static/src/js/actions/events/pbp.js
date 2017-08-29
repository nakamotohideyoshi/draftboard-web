// import merge from 'lodash/merge';
import filter from 'lodash/filter';
import log from '../../lib/logging';
import map from 'lodash/map';
import merge from 'lodash/merge';
import orderBy from 'lodash/orderBy';
import random from 'lodash/random';
import { addEventAndStartQueue } from '../events';
import { addOrdinal } from '../../lib/utils/numbers';
import { dateNow } from '../../lib/utils';
import { humanizeFP } from '../../lib/utils/numbers';
import { SPORT_CONST, isGameReady } from '../sports';

// get custom logger for actions
const logAction = log.getLogger('action');


/**
 * Parse the message content for any players involved
 * @param  {object} message Pusher event message
 * @param  {string} sport   Sport, based on available actions.sport.SPORT_CONST
 * @return {array}          List of players
 */
const compileMLBEventPlayers = (message, sport) => {
  logAction.trace('actions.compileMLBEventPlayers', sport);

  const eventPlayers = [
    message.pbp.srid_pitcher,  // pitcher
    message.at_bat.srid_hitter,  // hitter
  ];

  // runners on base
  if (Array.isArray(message.runners)) {
    message.runners.map((runner) => eventPlayers.push(runner.srid));
  }

  return eventPlayers;
};

const consolidateZonePitches = (zonePitches) => {
  logAction.trace('actions.consolidateZonePitches');

  const sportConst = SPORT_CONST.mlb;
  const filtered = filter(zonePitches, (pitch) => pitch.hasOwnProperty('mph'));
  const sorted = orderBy(filtered, 'pc');

  // could make this dynamic, but faster if we just write it out for now
  return map(sorted, (pitch) => {
    // randomize position of pitch within zone
    const zone = pitch.z;
    let left = 0;
    let top = 0;

    // left
    switch (zone) {
      case 1:
      case 4:
      case 7:
        left = random(-4, 22);
        break;
      case 2:
      case 5:
      case 8:
        left = random(30, 55);
        break;
      case 3:
      case 6:
      case 9:
        left = random(64, 88);
        break;
      case 10:
        left = random(98, 108);
        break;
      case 12:
        left = random(-24, -12);
        break;
      case 11:
      case 13:
        left = random(-2, 88);
        break;
      default:
        left = 0;
    }

    // top
    switch (zone) {
      case 1:
      case 2:
      case 3:
        top = random(-2, 23);
        break;
      case 4:
      case 5:
      case 6:
        top = random(31, 56);
        break;
      case 7:
      case 8:
      case 9:
        top = random(65, 90);
        break;
      case 11:
        top = random(98, 108);
        break;
      case 13:
        top = random(-20, -10);
        break;
      case 10:
      case 12:
        top = random(-2, 90);
        break;
      default:
        top = 0;
    }

    return {
      count: pitch.pc,
      outcome: (pitch.z < 10) ? 'strike' : 'ball',
      speed: pitch.mph,
      type: sportConst.pitchTypes[pitch.t],
      zone: pitch.z,
      left,
      top,
    };
  });
};

/**
 * TODO move to lib.utils
 *
 * Helper method to convert an object of pitch types into a readable sentence
 * Example pitchCount:
 * "count__list": {
 *    "pitch_count": 5,
 *    "strikes": 1,
 *    "balls": 3,
 *    "outs": 3
 *  },
 * @param  {object} pitchCount Types of pitches and their count, defaults all to 0
 * @return {string}            Human readable pitch count
 */
export const stringifyAtBat = (pitchCount) => {
  const { b = 0, k = 0, outs = 0 } = pitchCount;

  // if everything is defaults, then return false
  if (b === k === outs === 0) return false;

  return `${b}B/${k}S - ${outs} Outs`;
};

/**
 * TODO move to lib.utils
 *
 * Returns string stating when event occurred in game
 *
 * @param  {number} inning Loose number of inning, eg '5.0'
 * @param  {string} half   Bottom or top of inning, denoted with 'B', 'T', respectively
 * @return {string}        Readable version of when, eg 'Bottom of 5th', or false if it has not started
 */
export const stringifyMLBWhen = (inning, half) => {
  const when = (half === 'B') ? 'Bottom' : 'Top';

  const inningWIthOrdinal = addOrdinal(inning);

  if (inningWIthOrdinal === false) return false;

  if (half) {
    return `${when} of ${inningWIthOrdinal}`;
  }

  return inningWIthOrdinal;
};

/**
 * Check whether we would even want to use this PBP
 * @param  {object} message Pusher event message
 * @param  {string} sport   Sport, based on available actions.sport.SPORT_CONST
 * @return {boolean}        True if we want to use, false if we don't
 */
const validateMLBMessage = (message) => {
  logAction.debug('actions.isMessageUsed');

  const reasons = [];

  // only working with at bats
  if (!('srid_at_bat' in message.pbp)) reasons.push('!message.pbp.srid_at_bat');
  if (typeof message.at_bat !== 'object' || !('srid_hitter' in message.at_bat)) {
    reasons.push('!message.at_bat.srid_hitter');
  }
  // if the at bat is over, then there must be a description
  // if (message.pbp.flags.is_ab_over === true && !message.at_bat.oid_description) {
  //   reasons.push('!message.at_bat.oid_description');
  // }
  return reasons.length < 1;
};

/*
 * Converts `mlb_pbp.linked` to the relevant data we need
 *
 * @param  {object} message  The received event from Pusher
 * @param  {string} gameId   Game SRID
 * @param  {object} boxscore Boxscore object for inning data
 */
const getMLBData = (message, gameId, boxscore) => {
  logAction.trace('actions.getMLBData');

  // faster to not camelize the object
  /* eslint-disable camelcase */
  const { at_bat = {}, pbp = {}, runners = [], stats = {}, zone_pitches = [] } = message;
  const { stats_str = '', fn = '', ln = '', srid_team, srid_hitter } = at_bat;
  const { count = {}, flags = {}, srid_at_bat, srid_pitcher } = pbp;
  /* eslint-enable camelcase */

  return {
    description: at_bat.oid_description || '',
    eventPlayers: compileMLBEventPlayers(message, 'mlb'),
    gameId,
    hitter: {
      atBatStats: stats_str,
      name: `${fn} ${ln}`,
      sridPlayer: srid_hitter,
      sridTeam: srid_team,
      outcomeFp: humanizeFP(at_bat.oid_fp, true) || null,
    },
    id: pbp.srid,
    isAtBatOver: flags.is_ab_over || false,
    pitchCount: stringifyAtBat(count),
    pitcher: {
      sridPlayer: srid_pitcher,
      outcomeFp: humanizeFP(pbp.oid_fp, true) || null,
    },
    runnerIds: runners.map(runner => runner.srid),
    runners: runners.map((runner) => ({
      playerSrid: runner.srid,
      endingBase: runner.end,
      startingBase: runner.start,
      outcomeFp: humanizeFP(runner.oid_fp, true) || null,
    })),
    playersStats: stats || [],
    sport: 'mlb',
    sridAtBat: srid_at_bat,
    when: {
      half: boxscore.inning_half || false,
      inning: stringifyMLBWhen(boxscore.inning),
      humanized: stringifyMLBWhen(boxscore.inning, boxscore.inning_half),
    },
    zonePitches: consolidateZonePitches(zone_pitches),
  };
};

/*
 * Converts the provided message to a PBP message.
 * @param  {object} message  The received event from Pusher
 * @param  {string} gameId   Game SRID
 * @param  {string} sport    The sport associated with the PBP.
 */
const getPBPData = (message, gameId, sport) => (
  merge(message, {
    sport,
    gameId,
    id: message.pbp.id,
    eventPlayers: message.stats.map(stat => stat.srid_player),
    playersStats: message.stats || [],
    type: message.pbp.type,
  })
);

/*
 * Take a pusher call, validate, then reshape to fit into store.events
 * `message` depends on sport:
 * - MLB `mlb_pbp.linked` docs here https://git.io/vofyM
 * - MLB `mlb_pbp.event` docs here https://git.io/vofyD
 * - NBA `nba_pbp.linked` docs here https://git.io/vofyy
 *
 * @param  {object} message The received event from Pusher
 */
export const onPBPReceived = (message, sport) => (dispatch, getState) => {
  logAction.debug('actions.onPBPReceived', message, sport);

  let pbpData;
  const gameId = message.pbp.srid_game;

  if (sport !== 'mlb') {
    pbpData = getPBPData(message, gameId, sport);
  } else {
    const state = getState();
    if (!isGameReady(state, dispatch, sport, gameId) || !validateMLBMessage(message)) {
      return false;
    }
    const boxscore = state.sports.games[gameId].boxscore;
    pbpData = getMLBData(message, gameId, boxscore);
  }

  return dispatch(addEventAndStartQueue(gameId, pbpData, 'pbp', sport));
};

/*
 * Shortcut method to pull events into linked, as it's a subset of linked anyways
 */
export const onPBPEventReceived = (message, sport) => (dispatch) => {
  logAction.debug('actions.onPBPEventReceived');

  const linkedMessage = {
    pbp: message,
  };

  return dispatch(onPBPReceived(linkedMessage, sport));
};
