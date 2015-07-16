"use strict";

// Pull in the main scss file.
require("app.scss");

//var config = require("config");
var log = require("lib/logging");
log.debug('Bootstrapping app via app.jsx');

require('actions/keypress-actions');

// Add top-level react components to the app, any dependencies of those components will be loaded also.
require("components/form-field/ssn");
require("components/site/hamburger-menu");
require("components/site/app-state-class");
require("components/contest-list/contest-list");
require("components/contest-nav/contest-nav.jsx");
