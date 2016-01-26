// Sentry error reporting.
import Raven from 'raven-js';
Raven.config('https://698f3f69f1e446cea667c680c4e1931b@app.getsentry.com/40103', {
  // Whitelist all of our heroku instances.
  whitelistUrls: [/draftboard-.*\.herokuapp\.com/]
}).install();


// Pull in the main scss file.
require("app.scss");

//var config = require("config");
var log = require("lib/logging");
log.debug('Bootstrapping app via app.jsx');

// before we execute anything else, wipe the redux entry in localStorage if asked.
if (window.dfs.wipeRedux === "1") {
    log.debug('store.js - Wiping localStorage due to query param')
    window.localStorage.clear()
}

require('actions/keypress-actions');

// Add top-level react components to the app, any dependencies of those components will be loaded
// also.
require("components/account/deposits.jsx");
require("components/account/settings.jsx");
require("components/account/sidebar.jsx");
require("components/account/transactions.jsx");
require("components/account/withdrawals.jsx");


require("components/form-field/ssn");
require("components/site/pane.js");
require("components/site/message-display.jsx");

// Lobby
require("components/nav-scoreboard/nav-scoreboard.jsx");
require("components/lobby/lobby-contests.jsx");
require("components/lobby/lobby-lineup-card-list.jsx");

// Draft
require("components/draft/draft-lineup-card-list.jsx");
require("components/draft/draft-player-list.jsx");

// Top level components for the live section
require("components/live/live");

// Results
require("components/results/results");
