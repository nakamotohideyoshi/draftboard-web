/**
 *   Responsible for combining all the system's reducers in a
 * single place.
 */

const { combineReducers } = require('redux');

const contests = require('./contests');
const draftDraftGroup = require('./draft-groups');
const upcomingLineups = require('./lineups');
const createLineup = require('./create-lineup.js');

module.exports = combineReducers({
  contests,
  draftDraftGroup,
  upcomingLineups,
  createLineup
});
