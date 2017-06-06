import log from '../../lib/logging';
import { addEventAndStartQueue } from '../events';
import { updatePlayerStats } from '../live-draft-groups';
import { isGameReady } from '../sports';

// get custom logger for actions
const logAction = log.getLogger('action');


/*
 * When we receive a Pusher stats call, make sure it's related to our games/players, and if so send to the appropriate
 * method to be parsed
 * `stats.player` message depends on sport:
 * - MLB `mlb_stats.player` hitter docs here https://git.io/vofy6
 * - MLB `mlb_stats.player` pitcher docs here https://git.io/vofDG
 * - NBA `nba_stats.player` docs here https://git.io/vofyi
 * - NFL `nfl_stats.player` docs here https://git.io/vKlSG
 *
 * @param  {object} message        The received message from Pusher
 * @param  {string} sport          The player's sport, used to parse in actions
 * @param  {integer} draftGroupId  Draft group the player is in
 * @param  {object} relevantGames  Games we would need to animate
 */
export const onPlayerStatsReceived = (message, sport, relevantGames) => (dispatch, getState) => {
  logAction.debug('actions.onPlayerStatsReceived', message);

  const gameId = message.srid_game;

  if (!isGameReady(getState(), dispatch, sport, gameId)) return false;

  // if it's not a relevant game to the live section, then just update the player's FP to update the NavScoreboard
  if (relevantGames.indexOf(gameId) === -1) return dispatch(updatePlayerStats(sport, message));

  return dispatch(addEventAndStartQueue(gameId, message, 'stats', sport));
};
