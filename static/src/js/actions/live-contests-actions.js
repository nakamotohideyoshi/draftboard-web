"use strict";

var Reflux = require("reflux");

var LiveContestsActions = Reflux.createActions({
  "loadContest": {children: ["completed", "status", "failed"]},
  "loadContestInfo": {children: ["completed", "failed"]},
  "loadContestLineups": {children: ["completed", "failed"]}
});


module.exports = LiveContestsActions;
