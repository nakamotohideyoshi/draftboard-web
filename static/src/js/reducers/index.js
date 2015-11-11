/**
 *   Responsible for combining all the system's reducers in a
 * single place.
 */

const { combineReducers } = require('redux')

const contests = require('./contests')
const draftDraftGroup = require('./draft-group')
const upcomingDraftGroups = require('./upcoming-draft-groups.js')
const upcomingLineups = require('./lineups')
const upcomingContests = require('./upcoming-contests.js')
const createLineup = require('./create-lineup.js')
const entries = require('./entries')

module.exports = combineReducers({
  contests,
  entries,
  draftDraftGroup,
  upcomingLineups,
  upcomingContests,
  upcomingDraftGroups,
  createLineup
})
