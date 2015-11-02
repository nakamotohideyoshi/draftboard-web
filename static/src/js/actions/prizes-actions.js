"use strict";

var Reflux = require("reflux");


var PrizesActions = Reflux.createActions({
  "loadPrize": {children: ["completed", "failed"]}
});


module.exports = PrizesActions;
