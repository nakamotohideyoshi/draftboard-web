import { createSelector } from 'reselect';
import _ from 'lodash';

import { liveContestsSelector } from './live-contests';
import { currentLineupsSelector, compileRosterStats, compileVillianLineup } from './current-lineups';
import { GAME_DURATIONS } from '../actions/sports';


/**
 * Take the current contest and return two lists, one with all players by ownership, and the other the top 8 not owned
 * by me.
 * @param  {object} contest  Contest object
 * @param  {string} sport    Which sport the contest is for, used to determine default roster length
 * @param  {list}   myRoster Roster to filter out players with
 * @return {object}          All players and top 8 players not in my lineup
 */
const calculatePlayerOwnership = (contest, draftGroup, sport, games, myRoster) => {
  const numOfPlayers = GAME_DURATIONS[sport].players;

  const lineups = _.filter(contest.lineups, (lineup) => lineup.roster[0] !== 0);
  const allPlayers = _.flatten(_.map(lineups, (lineup) => lineup.roster));
  const counts = _.countBy(allPlayers, (playerId) => playerId);

  // all
  const mappedPlayers = _.map(counts, (ownershipCount, playerId) => ({
    ownershipCount,
    playerId,
    ownershipPercent: parseInt(ownershipCount / allPlayers.length * 100, 10),
  }));
  const allPlayersByCounts = _.sortBy(mappedPlayers, (playerWithCount) => playerWithCount.ownershipCount).reverse();

  // filter to players not owned by me
  const nonOwnedByMe = _.filter(allPlayersByCounts, (player) => myRoster.indexOf(player.playerId) === -1);
  let top8 = _.sortBy(nonOwnedByMe, (playerWithCount) => playerWithCount.ownershipCount);

  // return top 8 not owned by me, if there are 8 to use, otherwise return all
  if (top8.length > numOfPlayers) {
    top8 = top8.slice(0, numOfPlayers);
  } else {
    top8 = allPlayersByCounts.slice(0, numOfPlayers);
  }
  top8 = _.map(top8, (p) => p.playerId);

  // return players with their stats
  const allWithStats = compileRosterStats(allPlayers, draftGroup, games, []);

  // combine counts with data
  const all = _.map(allPlayersByCounts, (playerWithCount) => Object.assign(
    playerWithCount,
    allWithStats[playerWithCount.playerId]
  ));

  const allByPlayerId = {};
  _.forEach(mappedPlayers, (playerWithCount) => {
    allByPlayerId[playerWithCount.playerId] = playerWithCount.ownershipPercent;
  });

  return {
    all,
    top8,
    allByPlayerId,
  };
};


/**
 * Fancy Redux reselect selector that compiles together relevant live information.
 * Returns an object with an architecture of:
 *
 * lineups
 *   mine
 *   opponent (optional)
 * contest
 */
export const liveSelector = createSelector(
  liveContestsSelector,
  currentLineupsSelector,
  state => state.live.mode,
  state => state.entries,
  state => state.playerBoxScoreHistory,
  state => state.liveDraftGroups,
  state => state.sports,

  (contestStats, currentLineupsStats, mode, entries, playerBoxScoreHistory, liveDraftGroups, sports) => {
    const uniqueEntries = _.uniq(_.values(entries.items), 'lineup');

    const stats = {
      hasRelatedInfo: false,
      lineups: {},
      mode,
      relevantGames: [],
      relevantPlayers: [],
      entries: uniqueEntries,
    };

    if (entries.hasRelatedInfo === false) {
      return stats;
    }
    stats.hasRelatedInfo = true;

    if (mode.myLineupId) {
      const myLineup = currentLineupsStats[mode.myLineupId];
      const sport = myLineup.draftGroup.sport;

      // add in seasonal stats, teams for LivePlayerPane
      _.forEach(myLineup.rosterDetails, (player, playerId) => {
        if (playerBoxScoreHistory.nba.hasOwnProperty(playerId) === true) {
          myLineup.rosterDetails[playerId].seasonalStats = playerBoxScoreHistory.nba[playerId];
        }

        myLineup.rosterDetails[playerId].teamInfo = sports[sport].teams[player.info.team_srid];
      });

      // combine relevant players, games to target pusher calls for animations
      stats.relevantGames = _.union(
        stats.relevantGames,
        _.map(myLineup.rosterDetails, (player) => player.info.game_srid)
      );
      stats.relevantPlayers = _.union(
        stats.relevantPlayers,
        _.map(myLineup.rosterDetails, (player) => player.info.player_srid)
      );


      // add in draft group to update player stats with pusher
      stats.draftGroup = liveDraftGroups[myLineup.draftGroup.id];


      if (mode.contestId) {
        const contest = contestStats[mode.contestId];

        contest.playersOwnership = calculatePlayerOwnership(
          contest,
          stats.draftGroup,
          sport,
          sports.games,
          myLineup.roster
        );

        // add ownership % to lineup
        _.forEach(myLineup.rosterDetails, (player, playerId) => {
          myLineup.rosterDetails[playerId].ownershipPercent = contest.playersOwnership.allByPlayerId[playerId];
        });

        myLineup.myWinPercent = 0;
        if (myLineup.rank && contest.entriesCount) {
          myLineup.myWinPercent = myLineup.rank / contest.entriesCount * 100;
        }

        if (mode.opponentLineupId) {
          if (mode.opponentLineupId === 1) {
            contest.lineups[1] = compileVillianLineup(
              contest.playersOwnership.top8,
              stats.draftGroup,
              sport,
              sports.games
            );
          }

          const opponentLineup = contest.lineups[mode.opponentLineupId];

          _.forEach(opponentLineup.rosterDetails, (player, playerId) => {
            if (playerBoxScoreHistory.nba.hasOwnProperty(playerId) === true) {
              opponentLineup.rosterDetails[playerId].seasonalStats = playerBoxScoreHistory.nba[playerId];
            }

            opponentLineup.rosterDetails[playerId].teamInfo = sports[sport].teams[player.info.team_srid];

            // add ownership % to lineup
            opponentLineup.rosterDetails[playerId].ownershipPercent = contest.playersOwnership.allByPlayerId[playerId];
          });

          opponentLineup.opponentWinPercent = opponentLineup.rank / contest.entriesCount * 100;

          // used for animations to determine which side
          opponentLineup.rosterBySRID = _.map(opponentLineup.rosterDetails, (player) => player.info.player_srid);

          stats.relevantGames = _.union(
            stats.relevantGames,
            _.map(opponentLineup.rosterDetails, (player) => player.info.game_srid)
          );
          stats.relevantPlayers = _.union(
            stats.relevantPlayers,
            _.map(opponentLineup.rosterDetails, (player) => player.info.player_srid)
          );
          stats.playersInBothLineups = _.intersection(myLineup.rosterBySRID, opponentLineup.rosterBySRID);
          stats.lineups.opponent = opponentLineup;
        }

        // update potential earnings of normal lineup
        myLineup.potentialEarnings = contest.lineups[mode.myLineupId].potentialEarnings;

        stats.contest = contest;
      }

      stats.lineups.mine = myLineup;
    }

    return stats;
  }
);
