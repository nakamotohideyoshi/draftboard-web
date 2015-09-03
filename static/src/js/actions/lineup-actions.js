"use strict";

var Reflux = require("reflux");


var LineupActions = Reflux.createActions({
  "load": {children: ["completed", "failed"]},
  "lineupFocused": {}
});


module.exports = LineupActions;
