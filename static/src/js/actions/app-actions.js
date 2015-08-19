"use strict";

var Reflux = require("reflux");


/*
* Application-level actions. The idea for these is to provide a way to control
* app-wide state via the appStateStore.
*/
var AppActions = Reflux.createActions([
  'openNavMain',
  'closeNavMain',
  'openPane',
  'closePane'
]);


module.exports = AppActions;
