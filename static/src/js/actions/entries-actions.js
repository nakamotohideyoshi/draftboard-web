"use strict";

var Reflux = require("reflux");


var EntriesActions = Reflux.createActions({
  "loadEntries": {children: ["completed", "failed"]}
});


module.exports = EntriesActions;
