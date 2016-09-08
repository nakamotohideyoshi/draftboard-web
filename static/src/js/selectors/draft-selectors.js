import { createSelector } from 'reselect';
import { isPlayerInLineup } from '../components/draft/draft-utils.js';
import merge from 'lodash/merge';
import orderBy from 'lodash/orderBy';
import find from 'lodash/find';

const focusedPlayerIdSelector = (state) => state.draftGroupPlayersFilters.focusedPlayerId;
const allPlayersSelector = (state) => state.draftGroupPlayers.allPlayers;
const sportSelector = (state) => state.draftGroupPlayers.sport;
const draftGroupUpdatesSelector = (state) => state.draftGroupUpdates;
const playerBoxScoreHistorySelector = (state) => state.playerBoxScoreHistory;
const boxScoreGamesSelector = (state) => state.upcomingDraftGroups.boxScores;
const activeDraftGroupIdSelector = (state) => state.upcomingDraftGroups.activeDraftGroupId;
const sportInfoSelector = (state) => state.sports;
const availablePositionSelector = (state) => state.createLineup.availablePositions;
const newLineupSelector = (state) => state.createLineup.lineup;


/**
 * In the draft section, when you click on a player they become 'focused'. This selector gathers
 * up all the info needed to render the player detail pane.
 */
export const focusedPlayerSelector = createSelector(
  focusedPlayerIdSelector,
  allPlayersSelector,
  draftGroupUpdatesSelector,
  playerBoxScoreHistorySelector,
  boxScoreGamesSelector,
  sportSelector,
  activeDraftGroupIdSelector,
  sportInfoSelector,
  availablePositionSelector,
  newLineupSelector,
  (focusedPlayerId, allPlayers, draftGroupUpdates, playerBoxScoreHistory, boxScoreGames, sport, activeDraftGroupId,
    sportInfo, availablePositions, newLineup
  ) => {
    // if no player is focused, return nothing.
    if (!focusedPlayerId) {
      return null;
    }

    if (!allPlayers[focusedPlayerId]) {
      return null;
    }

    const focusedPlayer = allPlayers[focusedPlayerId];

    const player = merge({}, focusedPlayer, {
      sport,
      news: {},
      nextGame: {},
      boxScoreHistory: {},
      splitsHistory: [],
    });

    // Attach any news stories to the player object.
    if (sport in draftGroupUpdates &&
      'playerUpdates' in draftGroupUpdates[sport] &&
      'injury' in draftGroupUpdates[sport].playerUpdates
    ) {
      player.news = draftGroupUpdates[sport].playerUpdates.injury[focusedPlayer.player_srid];
    }

    // Attach player boxscore history to the player object.
    if (playerBoxScoreHistory.hasOwnProperty(sport)) {
      if (playerBoxScoreHistory[sport].hasOwnProperty(focusedPlayer.player_id)) {
        player.boxScoreHistory = playerBoxScoreHistory[sport][focusedPlayer.player_id];

        // If we have boxscore info, attach splits history.
        if (activeDraftGroupId && boxScoreGames.hasOwnProperty(activeDraftGroupId)) {
          switch (sport) {
            case 'nba': {
              const playerTeam = sportInfo[sport].teams[player.team_srid];

              if (!player.boxScoreHistory.games) {
                player.splitsHistory = [];
                break;
              }

              player.splitsHistory = player.boxScoreHistory.games.map((game, i) => {
                // Figure out which team the opponent was.
                const awayTeam = find(sportInfo[sport].teams, { id: player.boxScoreHistory.away_id[i] });
                const homeTeam = find(sportInfo[sport].teams, { id: player.boxScoreHistory.home_id[i] });
                // start with the assumption that the home team is the opponent.
                let oppTeam = homeTeam;
                // if the home team is actually the player's team, the away team is the opp.
                if (homeTeam.id === playerTeam.id) {
                  oppTeam = awayTeam;
                }

                return {
                  assists: player.boxScoreHistory.assists[i],
                  blocks: player.boxScoreHistory.blocks[i],
                  date: player.boxScoreHistory.start[i],
                  fp: player.boxScoreHistory.fp[i],
                  opp: oppTeam.alias,
                  points: player.boxScoreHistory.points[i],
                  rebounds: player.boxScoreHistory.rebounds[i],
                  steals: player.boxScoreHistory.steals[i],
                  turnovers: player.boxScoreHistory.turnovers[i],
                  minutes: player.boxScoreHistory.minutes[i],
                };
              });

              break;
            }

            case 'nhl':
              if (!player.boxScoreHistory.games) {
                player.splitsHistory = [];
                break;
              }
              player.splitsHistory = player.boxScoreHistory.games.map((game, i) => ({
                // TODO: Add date and opponent info into focusedPlayerSelector - this needs to be
                // done server-side since we don't have ALL historical boxScores to pull from.
                date: player.boxScoreHistory.start[i],
                opp: 'opp',
                fp: player.boxScoreHistory.fp[i],
                goal: player.boxScoreHistory.goal[i],
                assist: player.boxScoreHistory.assist[i],
                blocks: player.boxScoreHistory.blk[i],
                sog: player.boxScoreHistory.sog[i],
                saves: player.boxScoreHistory.saves[i],
                ga: player.boxScoreHistory.ga[i],
              }));
              break;

            default:

          }
          // Now sort them by date since the server is dumb.
          player.splitsHistory = orderBy(player.splitsHistory, 'date', 'desc');
        }
      }
    }

    // Attach the player's team info.
    if (sportInfo.hasOwnProperty(sport) && sportInfo[sport].teams[player.team_srid]) {
      player.teamCity = sportInfo[sport].teams[player.team_srid].city;
      player.teamName = sportInfo[sport].teams[player.team_srid].name;
    }

    // attach next game info.
    if (activeDraftGroupId && boxScoreGames.hasOwnProperty(activeDraftGroupId)) {
      // Grab info about the player's next game.
      player.nextGame = boxScoreGames[activeDraftGroupId][player.game_srid];
      // If we have team info, attach the next teams in the next game.
      if (player.nextGame && sportInfo.hasOwnProperty(sport)) {
        // Add home team info
        if (sportInfo[sport].teams.hasOwnProperty(player.nextGame.srid_home)) {
          player.nextGame.homeTeam = sportInfo[sport].teams[player.nextGame.srid_home];
        }
        // Add away team info.
        if (sportInfo[sport].teams.hasOwnProperty(player.nextGame.srid_away)) {
          player.nextGame.awayTeam = sportInfo[sport].teams[player.nextGame.srid_away];
        }
      }
    }

    // Add draft status.
    let draftable = true;
    let drafted = false;
    // Is there a slot available?
    if (availablePositions.indexOf(player.position) === -1) {
      draftable = false;
    }
    // Is the player already drafted?
    if (isPlayerInLineup(newLineup, player)) {
      draftable = false;
      drafted = true;
    }
    player.drafted = drafted;
    player.draftable = draftable;


    return player;
  }
);
