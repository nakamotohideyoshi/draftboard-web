"use strict";

var Reflux = require("reflux");


var ContestActions = Reflux.createActions([
  "contestsUpdated",
  "contestFocused"
]);


module.exports = ContestActions;
