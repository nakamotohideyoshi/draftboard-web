"use strict";

var Reflux = require("reflux");


var LiveNBAActions = Reflux.createActions({
  "loadContestLineups": {children: ["completed", "failed"]},
  "loadDraftGroup": {children: ["completed", "failed"]},
  "loadDraftGroupFantasyPoints": {children: ["completed", "failed"]},
  "loadLineup": {children: ["completed", "failed"]}
});


module.exports = LiveNBAActions;
