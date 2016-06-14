import { routerReducer as routing } from 'react-router-redux';
import { combineReducers } from 'redux';

const asyncFailures = require('./async-failures');
const contestPoolEntries = require('./contest-pool-entries');
const createLineup = require('./create-lineup');
const currentDraftGroups = require('./current-draft-groups');
const currentLineups = require('./current-lineups');
const draftGroupPlayers = require('./draft-group-players');
const draftGroupPlayersFilters = require('./draft-group-players-filters');
const entries = require('./entries');
const events = require('./events');
const eventsMultipart = require('./events-multipart');
const fantasyHistory = require('./fantasy-history');
const featuredContests = require('./featured-contests');
const injuries = require('./injuries');
const lineupEditRequests = require('./lineup-edit-requests');
const lineupUsernames = require('./lineup-usernames');
const liveContests = require('./live-contests');
const liveDraftGroups = require('./live-draft-groups');
const livePlayers = require('./live-players');
const messages = require('./messages');
const payments = require('./payments');
const playerBoxScoreHistory = require('./player-box-score-history');
const playerNews = require('./player-news');
const pollingTasks = require('./polling-tasks');
const prizes = require('./prizes');
const results = require('./results');
const sports = require('./sports');
const transactions = require('./transactions');
const upcomingContests = require('./upcoming-contests');
const upcomingDraftGroups = require('./upcoming-draft-groups');
const upcomingLineups = require('./upcoming-lineups');
const user = require('./user');
const watching = require('./watching');


/**
 * Responsible for combining all the system's reducers in a
 * single place.
 */
export default combineReducers({
  asyncFailures,
  contestPoolEntries,
  createLineup,
  currentDraftGroups,
  currentLineups,
  draftGroupPlayers,
  draftGroupPlayersFilters,
  entries,
  fantasyHistory,
  featuredContests,
  injuries,
  lineupEditRequests,
  liveContests,
  liveDraftGroups,
  eventsMultipart,
  livePlayers,
  messages,
  payments,
  playerNews,
  playerBoxScoreHistory,
  pollingTasks,
  prizes,
  events,
  results,
  routing,
  sports,
  transactions,
  upcomingContests,
  upcomingDraftGroups,
  upcomingLineups,
  lineupUsernames,
  user,
  watching,
});
