import { createSelector } from 'reselect';


const bigPlaysQueueSelector = (state) => state.events.bigEvents;

export const bigPlaysSelector = createSelector(
  [bigPlaysQueueSelector],
  (bigPlays) => bigPlays.map((value, index) => {
    const bigPlay = bigPlays[index];

    // pull out FP changes
    bigPlay.playerFPChanges = {};

    if ('playersStats' in bigPlay) {
      bigPlay.playersStats.map(playerStats => {
        bigPlay.playerFPChanges[playerStats.fields.srid_player] = playerStats.fields.fp_change;
      });
    }

    return bigPlay;
  })
);
