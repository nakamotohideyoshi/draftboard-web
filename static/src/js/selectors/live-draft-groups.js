import Raven from 'raven-js';
import { GAME_DURATIONS } from '../actions/sports';


/**
 * Method to parse player information from draft group. Used to fill lineup selectors
 * @param  {object} draftGroup Reference to state.liveDraftGroups[draftGroup.id]
 * @param  {integer} playerId  Unique player id within draft group
 * @param  {object} gamesTimeRemaining  Object of games with time remaining
 * @return {object}            Relevant player information
 */
export const assembleCurrentPlayer = (id, draftGroup, gamesTimeRemaining) => {
  // if we don't have info on the player, there's nothing to show
  if (draftGroup.playersInfo.hasOwnProperty(id) === false) {
    Raven.captureException(
      `selectors.liveDraftGroups - player ${id} does not exist in draftGroup[${draftGroup.id}].playersInfo`
    );

    return {};
  }

  // info typically has the following fields: {
  //   fppg: 11.375,
  //   game_srid: "47dcf0e0-f141-458e-8ef2-31d8f5f4a357",
  //   name: "P.J. Hairston",
  //   player_id: 2,
  //   player_srid: "2733be7a-cfc6-4787-8405-371db5af0399",
  //   position: "SG",
  //   salary: 3000,
  //   start: "2016-03-18T00:00:00Z",
  //   team_alias: "MEM",
  //   team_srid: "583eca88-fb46-11e1-82cb-f4ce4684ea4c",
  // }
  const info = draftGroup.playersInfo[id];

  // stats typically has the following fields: {
  //   fp: 4.25,
  //   id: 1,
  //   pos: "SG",
  // }
  const stats = draftGroup.playersStats[id] || {};

  // default to 100% time remaining if we do not have game data yet
  const timeRemaining = gamesTimeRemaining[info.game_srid] || {
    decimal: 0.9999,
    duration: GAME_DURATIONS[draftGroup.sport].gameDuration,
  };

  return {
    fp: stats.fp || 0,
    gameSRID: info.game_srid,
    id,  // only used in react chrome console to identify player
    name: info.name,
    position: info.position,
    srid: info.player_srid,
    teamSRID: info.team_srid,  // only used in selectors.Live
    teamAlias: info.team_alias,  // only used in cmp.liveStandingsPane
    timeRemaining,
  };
};
