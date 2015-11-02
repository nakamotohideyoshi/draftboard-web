"use strict";

var Reflux = require("reflux");

var LivePlayersActions = Reflux.createActions({
  "loadPlayer": {children: ["completed", "failed"]}
});


module.exports = LivePlayersActions;
