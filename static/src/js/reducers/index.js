/**
 *   Responsible for combining all the system's reducers in a
 * single place.
 */

import { routeReducer as routing } from 'redux-simple-router'
const { combineReducers } = require('redux')


const contests = require('./contests')
const createLineup = require('./create-lineup')
const currentBoxScores = require('./current-box-scores')
const currentDraftGroups = require('./current-draft-groups')
const currentLineups = require('./current-lineups')
const draftGroupPlayers = require('./draft-group-players')
const entries = require('./entries')
const featuredContests = require('./featured-contests.js')
const fantasyHistory = require('./fantasy-history.js')
const injuries = require('./injuries.js')
const live = require('./live')
const liveContests = require('./live-contests')
const liveDraftGroups = require('./live-draft-groups')
const liveGameQueues = require('./live-game-queues')
const payments = require('./payments')
const prizes = require('./prizes')
const results = require('./results')
const sports = require('./sports')
const transactions = require('./transactions')
const upcomingContests = require('./upcoming-contests.js')
const upcomingDraftGroups = require('./upcoming-draft-groups.js')
const upcomingLineups = require('./lineups')
const lineupUsernames = require('./lineup-usernames')
const user = require('./user')

module.exports = combineReducers({
  contests,
  createLineup,
  currentBoxScores,
  currentDraftGroups,
  currentLineups,
  draftGroupPlayers,
  entries,
  fantasyHistory,
  featuredContests,
  injuries,
  live,
  liveContests,
  liveDraftGroups,
  liveGameQueues,
  payments,
  prizes,
  results,
  routing,
  sports,
  transactions,
  upcomingContests,
  upcomingDraftGroups,
  upcomingLineups,
  lineupUsernames,
  user
})
