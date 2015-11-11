"use strict";

/**
 *   Responsible for combining all the system's reducers in a
 * single place.
 */

const { combineReducers } = require('redux');

const contests = require('./contests');
const entries = require('./entries');


module.exports = combineReducers({
  contests,
  entries
});
