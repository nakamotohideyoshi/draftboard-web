import {matchFilter} from './filters'
import { createSelector } from 'reselect'
import {filter as _filter} from 'lodash'

// All the upcoming lineups in the state.
const allLineupsSelector = (state) => state.upcomingLineups.lineups
const lineupBeingEdited = (state) => state.upcomingLineups.lineupBeingEdited
const draftGroupId = (state) => state.upcomingLineups.draftGroupIdFilter


// filter the lineups by draft group.
export const LineupsByDraftGroupSelector = createSelector(
  [allLineupsSelector, draftGroupId, lineupBeingEdited],
  (collection, draftGroupId,lineupBeingEdited) => {
    if (draftGroupId) {
      return _filter(collection, function(lineup) {
        if (lineup.id == lineupBeingEdited) {
          return false
        }
        return lineup.draft_group == draftGroupId
      })
    } else {
      return collection
    }
  }
)
