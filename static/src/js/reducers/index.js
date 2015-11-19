/**
 *   Responsible for combining all the system's reducers in a
 * single place.
 */

const { combineReducers } = require('redux');


const contests = require('./contests')
const createLineup = require('./create-lineup.js')
const currentLineups = require('./current-lineups');
const draftDraftGroup = require('./draft-group')
const entries = require('./entries')
const liveContests = require('./live-contests');
const liveDraftGroups = require('./live-draft-groups');
const payments = require('./payments')
const transactions = require('./transactions')
const upcomingContests = require('./upcoming-contests.js')
const upcomingDraftGroups = require('./upcoming-draft-groups.js')
const upcomingLineups = require('./lineups')
const user = require('./user')


module.exports = combineReducers({
  contests,
  createLineup,
  currentLineups,
  draftDraftGroup,
  entries,
  liveContests,
  liveDraftGroups,
  payments,
  transactions,
  upcomingContests,
  upcomingDraftGroups,
  upcomingLineups,
  user
});
