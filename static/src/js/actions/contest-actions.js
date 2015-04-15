"use strict";

var Reflux = require("reflux");

var ContestActions = Reflux.createActions({
  "load": {children: ["completed", "failed"]},
  "contestFocused": {}
});

module.exports = ContestActions;
