import Raven from 'raven-js';
import Cookies from 'js-cookie';
import log from 'lib/logging';


// Sentry error reporting.
if (process.env.NODE_ENV !== 'debug') {
  Raven.config('https://698f3f69f1e446cea667c680c4e1931b@app.getsentry.com/40103', {
    // Whitelist all of our heroku instances.
    whitelistUrls: [/draftboard-.*\.herokuapp\.com/],
  }).install();
}

// Pull in the main scss file.
require('app.scss');

// before we execute anything else, wipe the redux entry in localStorage if asked.
if (window.dfs.wipeLocalStorage === '1') {
  log.info('store.js - Wiping localStorage due to query param');
  window.localStorage.clear();
}

// wipe localStorage if the user changes
if (Cookies.get('username') !== window.dfs.user.username) {
  log.info('store.js - Wiping localStorage due to new username existing');
  Cookies.set('username', window.dfs.user.username);
  window.localStorage.clear();
}

// Global
require('actions/keypress-actions');
require('components/site/pane')();
require('components/site/message-display');

// Settings
require('components/account/deposits');
require('components/account/settings');
require('components/account/sidebar');
require('components/account/transactions');
require('components/account/withdrawals');
require('components/form-field/ssn');

// Lobby
require('components/nav-scoreboard/nav-scoreboard');
require('components/lobby/lobby-contests');
require('components/lobby/lobby-lineup-card-list');

// Draft
require('components/draft/draft-lineup-card-list');
require('components/draft/draft-player-list');

// Live
require('components/live/live');

// Results
require('components/results/results');
