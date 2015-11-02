"use strict";

var Reflux = require("reflux");

var LiveLineupsActions = Reflux.createActions({
  "loadLineup": {children: ["completed", "failed"]},
});


module.exports = LiveLineupsActions;
