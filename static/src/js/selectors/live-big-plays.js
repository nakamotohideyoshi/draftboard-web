import { createSelector } from 'reselect';
import { sportsSelector } from './sports';


const bigPlaysQueueSelector = (state) => state.events.bigEvents;

export const bigPlaysSelector = createSelector(
  [bigPlaysQueueSelector, sportsSelector],
  (bigPlays, sports) => bigPlays.map((value, index) => {
    const bigPlay = bigPlays[index];
    const game = sports.games[bigPlay.gameId];

    // TODO change to camelcase in call
    const homeScore = game.home_score;
    const awayScore = game.away_score;

    bigPlay.homeScoreStr = `${game.homeTeamInfo.alias} ${homeScore}`;
    bigPlay.awayScoreStr = `${game.awayTeamInfo.alias} ${awayScore}`;
    bigPlay.winning = (homeScore > awayScore) ? 'home' : 'away';

    // pull out FP changes
    bigPlay.playerFPChanges = {};
    bigPlay.playersStats.map(playerStats => {
      bigPlay.playerFPChanges[playerStats.fields.srid_player] = playerStats.fields.fp_change;
    });

    return bigPlay;
  })
);
