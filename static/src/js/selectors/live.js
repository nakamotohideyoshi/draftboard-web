import { createSelector } from 'reselect';
import { countBy as _countBy } from 'lodash';
import { filter as _filter } from 'lodash';
import { flatten as _flatten } from 'lodash';
import { forEach as _forEach } from 'lodash';
import { intersection as _intersection } from 'lodash';
import { map as _map } from 'lodash';
import { merge as _merge } from 'lodash';
import { sortBy as _sortBy } from 'lodash';
import { uniq as _uniq } from 'lodash';
import { union as _union } from 'lodash';
import { values as _values } from 'lodash';
import { dateNow } from '../lib/utils';
import log from '../lib/logging';

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

  const lineups = _filter(contest.lineups, (lineup) => lineup.roster[0] !== 0);
  const allPlayers = _flatten(_map(lineups, (lineup) => lineup.roster));
  const counts = _countBy(allPlayers, (playerId) => playerId);

  // all
  const mappedPlayers = _map(counts, (ownershipCount, playerId) => ({
    ownershipCount,
    playerId,
    ownershipPercent: parseInt(ownershipCount / allPlayers.length * 100, 10),
  }));
  const allPlayersByCounts = _sortBy(mappedPlayers, (playerWithCount) => playerWithCount.ownershipCount).reverse();

  // filter to players not owned by me
  const nonOwnedByMe = _filter(allPlayersByCounts, (player) => myRoster.indexOf(player.playerId) === -1);
  let top8 = _sortBy(nonOwnedByMe, (playerWithCount) => playerWithCount.ownershipCount);

  // return top 8 not owned by me, if there are 8 to use, otherwise return all
  if (top8.length > numOfPlayers) {
    top8 = top8.slice(0, numOfPlayers);
  } else {
    top8 = allPlayersByCounts.slice(0, numOfPlayers);
  }
  top8 = _map(top8, (p) => p.playerId);

  // return players with their stats
  const allWithStats = compileRosterStats(allPlayers, draftGroup, games, []);

  // combine counts with data
  const all = _map(allPlayersByCounts,
    (playerWithCount) => _merge(
      playerWithCount,
      allWithStats[playerWithCount.playerId]
    )
  );

  const allByPlayerId = {};
  _forEach(mappedPlayers, (playerWithCount) => {
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
    const uniqueEntries = _uniq(_values(entries.items), 'lineup');

    const stats = {
      draftGroupEnded: false,
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

      if (myLineup === undefined) {
        log.warn('liveSelector - myLineup is undefined');
        return stats;
      }

      // this pairs up with addMessage in Live component to make user aware
      if (myLineup.draftGroup.end < dateNow()) {
        stats.draftGroupEnded = true;
      }

      const sport = myLineup.draftGroup.sport;

      // add in seasonal stats, teams for LivePlayerPane
      _forEach(myLineup.rosterDetails, (player, playerId) => {
        if (playerBoxScoreHistory.nba.hasOwnProperty(playerId) === true) {
          myLineup.rosterDetails[playerId].seasonalStats = playerBoxScoreHistory.nba[playerId];
        }

        myLineup.rosterDetails[playerId].teamInfo = sports[sport].teams[player.info.team_srid];
      });

      // combine relevant players, games to target pusher calls for animations
      stats.relevantGames = _union(
        stats.relevantGames,
        _map(myLineup.rosterDetails, (player) => player.info.game_srid)
      );
      stats.relevantPlayers = _union(
        stats.relevantPlayers,
        _map(myLineup.rosterDetails, (player) => player.info.player_srid)
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
        _forEach(myLineup.rosterDetails, (player, playerId) => {
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

          _forEach(opponentLineup.rosterDetails, (player, playerId) => {
            if (playerBoxScoreHistory.nba.hasOwnProperty(playerId) === true) {
              opponentLineup.rosterDetails[playerId].seasonalStats = playerBoxScoreHistory.nba[playerId];
            }

            opponentLineup.rosterDetails[playerId].teamInfo = sports[sport].teams[player.info.team_srid];

            // add ownership % to lineup
            opponentLineup.rosterDetails[playerId].ownershipPercent = contest.playersOwnership.allByPlayerId[playerId];
          });

          opponentLineup.opponentWinPercent = opponentLineup.rank / contest.entriesCount * 100;

          // used for animations to determine which side
          opponentLineup.rosterBySRID = _map(opponentLineup.rosterDetails, (player) => player.info.player_srid);

          stats.relevantGames = _union(
            stats.relevantGames,
            _map(opponentLineup.rosterDetails, (player) => player.info.game_srid)
          );
          stats.relevantPlayers = _union(
            stats.relevantPlayers,
            _map(opponentLineup.rosterDetails, (player) => player.info.player_srid)
          );
          stats.playersInBothLineups = _intersection(myLineup.rosterBySRID, opponentLineup.rosterBySRID);
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
