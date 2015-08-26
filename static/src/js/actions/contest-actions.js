"use strict";

var Reflux = require("reflux");


var ContestActions = Reflux.createActions({
  "load": {children: ["completed", "failed"]},
  "contestFocused": {},
    // Register a filter with a DataTable.
  'registerFilter': {},
  // Tell the DataTable when a filter has been updated.
  'filterUpdated': {},
  // Clear out any active filters from a DataTable.
  'clearFilters': {},
  // Sort the list of contests.
  'sortByKey': {},
  // Activate the next visible row.
  'focusNextRow': {},
  // Activate the previous visible row.
  'focusPreviousRow': {},
  // The contest type filters have been selected - the other filters need to reveal.
  'contestTypeFiltered': {}
});


module.exports = ContestActions;
