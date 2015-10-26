"use strict";

var Reflux = require("reflux");


var LiveDraftGroupsActions = Reflux.createActions({
  "loadDraftGroup": {children: ["completed", "failed"]},
  "loadDraftGroupFantasyPoints": {children: ["completed", "failed"]}
});


module.exports = LiveDraftGroupsActions;
