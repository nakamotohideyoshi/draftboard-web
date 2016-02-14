import { createSelector } from 'reselect';

const focusedPlayerIdSelector = (state) => state.draftGroupPlayers.focusedPlayer;
const sportSelector = (state) => state.draftGroupPlayers.sport;
const playerNewsSelector = (state) => state.playerNews;
const playerBoxScoreHistorySelector = (state) => state.playerBoxScoreHistory;
const boxScoreGamesSelector = (state) => state.upcomingDraftGroups.boxScores;
const activeDraftGroupIdSelector = (state) => state.upcomingDraftGroups.activeDraftGroupId;
const sportInfoSelector = (state) => state.sports;


/**
 * In the draft section, when you click on a player they become 'focused'. This selector gathers
 * up all the info needed to render the player detail pane.
 */
export const focusedPlayerSelector = createSelector(
  focusedPlayerIdSelector,
  playerNewsSelector,
  playerBoxScoreHistorySelector,
  boxScoreGamesSelector,
  sportSelector,
  activeDraftGroupIdSelector,
  sportInfoSelector,
  (focusedPlayer, playerNews, playerBoxScoreHistory, boxScoreGames, sport, activeDraftGroupId, sportInfo) => {
    // if no player is focused, return nothing.
    if (!focusedPlayer) {
      return null;
    }

    const player = Object.assign({}, focusedPlayer, {
      sport,
      news: {},
      nextGame: {},
      boxScoreHistory: {},
      splitsHistory: [],
    });

    // Attach any news stories to the player object.
    if (playerNews.hasOwnProperty(sport)) {
      if (playerNews[sport].hasOwnProperty(focusedPlayer.player_id)) {
        player.news = playerNews[sport][focusedPlayer.player_id].news;
      }
    }

    // Attach player boxscore history to the player object.
    if (playerBoxScoreHistory.hasOwnProperty(sport)) {
      if (playerBoxScoreHistory[sport].hasOwnProperty(focusedPlayer.player_id)) {
        player.boxScoreHistory = playerBoxScoreHistory[sport][focusedPlayer.player_id];

        // If we have boxscore info, attach splits history.
        if (activeDraftGroupId && boxScoreGames.hasOwnProperty(activeDraftGroupId)) {
          player.splitsHistory = player.boxScoreHistory.games.map((game, i) => ({
            // TODO: Add date and opponent info into focusedPlayerSelector - this needs to be
            // done server-side since we don't have ALL historical boxScores to pull from.
            assists: player.boxScoreHistory.assists[i],
            blocks: player.boxScoreHistory.blocks[i],
            date: player.boxScoreHistory.start[i],
            fp: player.boxScoreHistory.fp[i],
            opp: 'opp',
            points: player.boxScoreHistory.points[i],
            rebounds: player.boxScoreHistory.rebounds[i],
            steals: player.boxScoreHistory.steals[i],
            three_pointers: player.boxScoreHistory.three_points_made[i],
            turnovers: player.boxScoreHistory.turnovers[i],
          }));
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

    return player;
  }
);
