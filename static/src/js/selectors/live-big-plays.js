import { createSelector } from 'reselect';

const bigPlaysQueueSelector = (state) => state.events.bigEvents;

export const bigPlaysSelector = createSelector([bigPlaysQueueSelector], (bigPlays) => (
  bigPlays.map((value, index) => bigPlays[index])
));
