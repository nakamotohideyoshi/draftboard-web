import Raven from 'raven-js';
import 'babel-polyfill';
import Cookies from 'js-cookie';
import log from 'lib/logging';

// Sentry error reporting.
//
// Set the default Sentry project as Draftboard - Local. If we aren't in debug mode, change it to
// the Draftboard - Staging project.
// the DSN for the Draftboard - Local Sentry Project
let sentryDSN = 'https://bbae8e8654e34a80b02999b5ade6fd81@app.getsentry.com/72241';

if (process.env.NODE_ENV === 'production') {
  // the DSN for the Draftboard - Staging Sentry Project
  sentryDSN = 'https://698f3f69f1e446cea667c680c4e1931b@app.getsentry.com/40103';
}

Raven.config(sentryDSN, {
  release: window.dfs.gitCommitUUID,
  tags: {
    git_commit: window.dfs.gitCommitUUID,
    pusher_key: window.dfs.user.pusher_key,
  },
  ignoreErrors: [
    // This is generally a pusher disconnection due to things like the user closing their laptop.
    'Error: Request has been terminated',
  ],
  // Whitelist all of our heroku instances.
  // whitelistUrls: [/draftboard-.*\.herokuapp\.com/],
}).install();

// Send any unhandled promise rejections to Sentry.
// https://docs.getsentry.com/hosted/clients/javascript/usage/#promises
window.onunhandledrejection = (evt) => {
  log.error(evt.reason);
  Raven.captureException(evt.reason);
};
// Set user info.
if (window.dfs.user.isAuthenticated) {
  Raven.setUserContext({
    id: window.dfs.user.username,
  });
}

// Pull in the main scss file.
require('app.scss');

// before we execute anything else, wipe the redux entry in localStorage if asked.
if (window.dfs.wipeLocalStorage === '1') {
  log.info('app.jsx - Wiping localStorage due to query param');
  window.localStorage.clear();
}

if (window.localStorage.version !== window.dfs.gitCommitUUID) {
  log.info('app.jsx - Wiping localStorage due to new deployment');
  window.localStorage.clear();
}

// wipe localStorage if the user changes
if (Cookies.get('username') !== window.dfs.user.username) {
  log.info('app.jsx - Wiping localStorage due to new username existing');
  Cookies.set('username', window.dfs.user.username);
  window.localStorage.clear();
}

// set new version
window.localStorage.setItem('version', window.dfs.gitCommitUUID);

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

// Lobby
require('components/nav-scoreboard/nav-scoreboard');
require('components/lobby/lobby-contests');
require('components/lobby/lobby-lineup-card-list');

// Draft
require('components/draft/draft-lineup-card-list');
require('components/draft/draft-container');

// Live
require('components/live/live');

// Results
require('components/results/results');
