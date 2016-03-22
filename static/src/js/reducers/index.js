import { routeReducer as routing } from 'redux-simple-router';
import { combineReducers } from 'redux';

const createLineup = require('./create-lineup');
const currentDraftGroups = require('./current-draft-groups');
const currentLineups = require('./current-lineups');
const draftGroupPlayers = require('./draft-group-players');
const entries = require('./entries');
const entryRequests = require('./entry-request.js');
const fantasyHistory = require('./fantasy-history.js');
const featuredContests = require('./featured-contests.js');
const injuries = require('./injuries.js');
const lineupEditRequests = require('./lineup-edit-requests.js');
const lineupUsernames = require('./lineup-usernames');
const live = require('./live');
const liveContests = require('./live-contests');
const liveDraftGroups = require('./live-draft-groups');
const livePlayers = require('./live-players');
const messages = require('./messages.js');
const payments = require('./payments');
const playerBoxScoreHistory = require('./player-box-score-history.js');
const playerNews = require('./player-news.js');
const prizes = require('./prizes');
const pusherLive = require('./pusher-live');
const results = require('./results');
const sports = require('./sports');
const transactions = require('./transactions');
const upcomingContests = require('./upcoming-contests.js');
const upcomingDraftGroups = require('./upcoming-draft-groups.js');
const upcomingLineups = require('./upcoming-lineups');
const user = require('./user');


/**
 * Responsible for combining all the system's reducers in a
 * single place.
 */
export default combineReducers({
  createLineup,
  currentDraftGroups,
  currentLineups,
  draftGroupPlayers,
  entries,
  entryRequests,
  fantasyHistory,
  featuredContests,
  injuries,
  lineupEditRequests,
  live,
  liveContests,
  liveDraftGroups,
  livePlayers,
  messages,
  payments,
  playerNews,
  playerBoxScoreHistory,
  prizes,
  pusherLive,
  results,
  routing,
  sports,
  transactions,
  upcomingContests,
  upcomingDraftGroups,
  upcomingLineups,
  lineupUsernames,
  user,
});
