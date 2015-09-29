"use strict";

var Reflux = require("reflux");


var DraftActions = Reflux.createActions({
  "loadDraftGroup": {children: ["completed", "failed"]},
  "saveLineup": {children: ["completed", "failed"]},
  "addPlayerToLineup": {},
  "removePlayerToLineup": {},
  "playerFocused": {}
});


module.exports = DraftActions;
