/**
 *   Responsible for combining all the system's reducers in a
 * single place.
 */

const { combineReducers } = require('redux');


const contests = require('./contests')
const createLineup = require('./create-lineup')
const currentLineups = require('./current-lineups');
const draftDraftGroup = require('./draft-group')
const entries = require('./entries')
const fantasyHistory = require('./fantasy-history.js')
const injuries = require('./injuries.js')
const live = require('./live')
const liveContests = require('./live-contests');
const liveDraftGroups = require('./live-draft-groups');
const prizes = require('./prizes')
const payments = require('./payments')
const transactions = require('./transactions')
const upcomingContests = require('./upcoming-contests.js')
const upcomingDraftGroups = require('./upcoming-draft-groups.js')
const upcomingLineups = require('./lineups')
const user = require('./user')
const results = require('./results')
import { routeReducer as routing } from 'redux-simple-router'


module.exports = combineReducers({
  contests,
  createLineup,
  currentLineups,
  draftDraftGroup,
  entries,
  fantasyHistory,
  injuries,
  live,
  results,
  liveContests,
  liveDraftGroups,
  payments,
  prizes,
  routing,
  transactions,
  upcomingContests,
  upcomingDraftGroups,
  upcomingLineups,
  user
});
