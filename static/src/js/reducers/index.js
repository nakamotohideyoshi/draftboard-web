/**
 *   Responsible for combining all the system's reducers in a
 * single place.
 */

const { combineReducers } = require('redux')

const contests = require('./contests')
const draftDraftGroup = require('./draft-groups')
const upcomingLineups = require('./lineups')
const upcomingContests = require('./upcoming-contests')
const createLineup = require('./create-lineup.js')
const entries = require('./entries')

module.exports = combineReducers({
  contests,
  entries,
  draftDraftGroup,
  upcomingLineups,
  upcomingContests,
  createLineup
})
