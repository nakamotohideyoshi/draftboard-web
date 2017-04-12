import { routerReducer as routing } from 'react-router-redux';
import { combineReducers } from 'redux';

const asyncFailures = require('./async-failures');
const contestPoolEntries = require('./contest-pool-entries');
const createLineup = require('./create-lineup');
const currentLineups = require('./current-lineups');
const draftGroupPlayers = require('./draft-group-players');
const draftGroupPlayersFilters = require('./draft-group-players-filters');
const events = require('./events');
const eventsMultipart = require('./events-multipart');
const fantasyHistory = require('./fantasy-history');
const featuredContests = require('./featured-contests');
const liveContests = require('./live-contests');
const liveContestPools = require('./live-contest-pools');
const liveDraftGroups = require('./live-draft-groups');
const livePlayers = require('./live-players');
const messages = require('./messages');
const payments = require('./payments');
const playerBoxScoreHistory = require('./player-box-score-history');
const playerAnalysisAndHistory = require('./player-analysis-history');
const prizes = require('./prizes');
const results = require('./results');
const sports = require('./sports');
const transactions = require('./transactions');
const contestPools = require('./contest-pools');
const upcomingDraftGroups = require('./upcoming-draft-groups');
const draftGroupUpdates = require('./draft-group-updates');
const upcomingLineups = require('./upcoming-lineups');
const user = require('./user');
const watching = require('./watching');


/**
 * Responsible for combining all the system's reducers in a
 * single place.
 */
export default combineReducers({
  asyncFailures,
  contestPools,
  contestPoolEntries,
  createLineup,
  currentLineups,
  draftGroupPlayers,
  draftGroupPlayersFilters,
  fantasyHistory,
  featuredContests,
  liveContests,
  liveContestPools,
  liveDraftGroups,
  eventsMultipart,
  livePlayers,
  messages,
  payments,
  playerBoxScoreHistory,
  playerAnalysisAndHistory,
  prizes,
  events,
  results,
  routing,
  sports,
  transactions,
  upcomingDraftGroups,
  draftGroupUpdates,
  upcomingLineups,
  user,
  watching,
});
