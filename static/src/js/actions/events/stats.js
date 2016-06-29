import log from '../../lib/logging';
import { addEventAndStartQueue } from '../events';
import { updatePlayerStats } from '../live-draft-groups';
import { isGameReady } from '../sports';


/*
 * When we receive a Pusher stats call, make sure it's related to our games/players, and if so send to the appropriate
 * method to be parsed
 * `stats.player` message depends on sport:
 * - MLB `mlb_stats.player` pitcher docs here https://git.io/vofDG
 * - MLB `mlb_stats.player` hitter docs here https://git.io/vofy6
 * - NBA `nba_stats.player` docs here https://git.io/vofyi
 *
 * @param  {object} message        The received message from Pusher
 * @param  {string} sport          The player's sport, used to parse in actions
 * @param  {integer} draftGroupId  Draft group the player is in
 * @param  {object} relevantGames  Games we would need to animate
 */
export const onPlayerStatsReceived = (message, sport, draftGroupId, relevantGames) => (dispatch, getState) => {
  log.trace('onPlayerStatsReceived', message);

  const gameId = message.fields.srid_game;

  if (!isGameReady(getState(), dispatch, sport, gameId)) return false;

  // if it's not a relevant game to the live section, then just update the player's FP to update the NavScoreboard
  if (relevantGames.indexOf(gameId) === -1) {
    // otherwise just update the player's FP
    return dispatch(updatePlayerStats(message, draftGroupId));
  }

  return dispatch(addEventAndStartQueue(gameId, message, 'stats', sport));
};
