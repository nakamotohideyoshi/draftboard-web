// Pull in the main scss file.
require("app.scss");

//var config = require("config");
var log = require("lib/logging");
log.debug('Bootstrapping app via app.jsx');

require('actions/keypress-actions');

// Add top-level react components to the app, any dependencies of those components will be loaded also.
require("components/account/deposits.jsx");
require("components/account/settings.jsx");
require("components/account/sidebar.jsx");
require("components/account/transactions.jsx");
require("components/account/withdrawals.jsx");


require("components/form-field/ssn");
require("components/site/hamburger-menu");
require("components/site/pane.js");

// Lobby
require("components/contest-nav/contest-nav.jsx");
require("components/lobby/lobby-contests.jsx");
require("components/lobby/lobby-lineup-card-list.jsx");

// Draft
require("components/draft/draft-lineup-card-list.jsx");
require("components/draft/draft-player-list.jsx");

// Top level components for the live section
require("components/live/live");
