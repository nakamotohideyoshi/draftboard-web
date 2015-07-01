"use strict";
/*
* A Wrapper for the loglevel module that sets the logging level based on our config file.
*/

var log = require("loglevel");
var config = require("../config");


log.setLevel(config.logLevel);


module.exports = log;
