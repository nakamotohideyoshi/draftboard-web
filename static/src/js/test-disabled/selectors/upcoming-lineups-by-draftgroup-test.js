import {LineupsByDraftGroupSelector} from '../../selectors/upcoming-lineups-by-draftgroup.js'
import {expect} from 'chai'

let store = {}

const initialStore = {
  upcomingLineups: {
    draftGroupIdFilter: null,
    lineupBeingEdited: null,
    lineups: {
      3: {
        id: 3,
        draft_group: 1
      },
      9: {
        id: 9,
        draft_group: 1
      },
      4: {
        id: 4,
        draft_group: 1
      },

      0: {
        id: 0,
        draft_group: 2
      }
    }
  }
}


describe('LineupsByDraftGroupSelector', () => {

  beforeEach(() => {
    // reset the state.
    store = initialStore
    store.upcomingLineups.draftGroupIdFilter = null
    store.upcomingLineups.lineupBeingEdited = null
  })


  it('should return all lineups if no draftGroupIdFilter or lineupBeingEdited is set', () => {
    let results = LineupsByDraftGroupSelector(store)
    expect(Object.keys(results).length).to.equal(4)
  })


  it('should filter based on draftGroupIdFilter', () => {
    store.upcomingLineups.draftGroupIdFilter = 1
    let results = LineupsByDraftGroupSelector(store)
    expect(Object.keys(results).length).to.equal(3)
  })


  it('should filter based on lineupBeingEdited & draftGroupIdFilter', () => {
    store.upcomingLineups.lineupBeingEdited = 9
    store.upcomingLineups.draftGroupIdFilter = 1
    let results = LineupsByDraftGroupSelector(store)
    expect(Object.keys(results).length).to.equal(2)

    // if there is only 1 in the draftgroup, and it's being edited, return 0
    store.upcomingLineups.lineupBeingEdited = 0
    store.upcomingLineups.draftGroupIdFilter = 2
    results = LineupsByDraftGroupSelector(store)
    expect(Object.keys(results).length).to.equal(0)
  })


  it('should ignore lineupBeingEdited if there is no draftGroupIdFilter', () => {
    store.upcomingLineups.lineupBeingEdited = 9
    let results = LineupsByDraftGroupSelector(store)
    expect(Object.keys(results).length).to.equal(4)
  })

})
