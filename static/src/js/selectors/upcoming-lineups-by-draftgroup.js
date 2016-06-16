import { createSelector } from 'reselect';
import filter from 'lodash/filter';

// All the upcoming lineups in the state.
const allLineupsSelector = (state) => state.upcomingLineups.lineups;
const lineupBeingEditedSelector = (state) => state.upcomingLineups.lineupBeingEdited;
const draftGroupIdSelector = (state) => state.upcomingLineups.draftGroupIdFilter;


// filter the lineups by draft group.
export const lineupsByDraftGroupSelector = createSelector(
  [allLineupsSelector, draftGroupIdSelector, lineupBeingEditedSelector],
  (collection, draftGroupId, lineupBeingEdited) => {
    if (draftGroupId) {
      return filter(collection, (lineup) => {
        if (lineup.id === lineupBeingEdited) {
          return false;
        }
        return String(lineup.draft_group) === String(draftGroupId);
      });
    }

    return collection;
  }
);
