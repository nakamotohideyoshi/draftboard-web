import mapValues from 'lodash/mapValues';
import size from 'lodash/size';
import { createSelector } from 'reselect';


const watchingSelector = (state) => state.watching;
const playerBoxScoreHistorySelector = (state) => state.playerBoxScoreHistory;
const sportsSelector = (state) => state.sports;

export const relevantPlayersSelector = (state) => state.livePlayers.relevantPlayers;

export const relevantPlayerBoxScoreHistoriesSelector = createSelector(
  [watchingSelector, relevantPlayersSelector, playerBoxScoreHistorySelector],
  (watching, players, histories) => {
    if (size(histories[watching.sport]) === 0 || size(players) === 0) return {};

    return mapValues(players, (player) => histories[watching.sport][player.id]);
  }
);

const watchingTeamsSelector = createSelector(
  [watchingSelector, sportsSelector],
  (watching, sports) => sports[watching]
);

export const relevantPlayerTeamsSelector = createSelector(
  [watchingSelector, relevantPlayersSelector, watchingTeamsSelector],
  (watching, players, teams) => {
    if (size(teams) === 0 || size(players) === 0) return {};

    return mapValues(players, (player) => teams[player.teamSRID]);
  }
);
