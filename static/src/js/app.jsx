import Raven from 'raven-js';
import 'babel-polyfill';
import Cookies from 'js-cookie';
import log from 'lib/logging';
require('../../../node_modules/moment/locale/en-gb.js');

// get custom logger for actions
const logApp = log.getLogger('app');


// Sentry error reporting.
// The environment-specific, public, Sentry DSN that is provided to us by the server via html.
const sentryDSN = window.dfs.sentryPublicDsn;

Raven.config(sentryDSN, {
  release: window.dfs.gitCommitUUID,
  tags: {
    git_commit: window.dfs.gitCommitUUID,
    pusher_key: window.dfs.user.pusher_key,
  },
  // These are mostly taken from https://gist.github.com/impressiver/5092952
  ignoreErrors: [
    // This is generally a pusher disconnection due to things like the user closing their laptop.
    'Request has been terminated',
    'NetworkError when attempting to fetch resource',
    // Random plugins/extensions
    'top.GLOBALS',
    // See: http://blog.errorception.com/2012/03/tale-of-unfindable-js-error.html
    'originalCreateNotification',
    'canvas.contentDocument',
    'MyApp_RemoveAllHighlights',
    'http://tt.epicplay.com',
    'Can\'t find variable: ZiteReader',
    'jigsaw is not defined',
    'ComboSearch is not defined',
    'http://loading.retry.widdit.com/',
    'atomicFindClose',
    // Facebook borked
    'fb_xd_fragment',
    // ISP "optimizing" proxy - `Cache-Control: no-transform` seems to reduce this. (thanks @acdha)
    // See http://stackoverflow.com/questions/4113268/how-to-stop-javascript-injection-from-vodafone-proxy
    'bmi_SafeAddOnload',
    'EBCallBackMessageReceived',
    // See http://toolbar.conduit.com/Developer/HtmlAndGadget/Methods/JSInjection.aspx
    'conduitPage',
    // Generic error code from errors outside the security sandbox
    // You can delete this if using raven.js > 1.0, which ignores these automatically.
    'Script error.',
    // Generic failed fetch attempt
    'Failed to fetch',
  ],
  ignoreUrls: [
    // Chrome extensions
    /extensions\//i,
    /^chrome:\/\//i,
    // Other plugins
    /127\.0\.0\.1:4001\/isrunning/i,  // Cacaoweb
    /webappstoolbarba\.texthelp\.com\//i,
    /metrics\.itunes\.apple\.com\.edgesuite\.net\//i,
  ],
  // Whitelist all of our heroku instances.
  // whitelistUrls: [/draftboard-.*\.herokuapp\.com/],
}).install();

// If Raven is not configured correctly...
if (Raven.ravenNotConfiguredError) {
  log.error(`Raven is not configured correctly! Current DSN is: "${sentryDSN}"`);
}

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
  logApp.info('app.jsx - Wiping localStorage due to query param');
  window.localStorage.clear();

// wipe localStorage if git commit changes
} else if (window.localStorage.version && window.localStorage.version !== window.dfs.gitCommitUUID) {
  logApp.info('app.jsx - Wiping localStorage due to new deployment');
  window.localStorage.clear();

// wipe localStorage if the user changes
} else if (Cookies.get('username') !== window.dfs.user.username) {
  logApp.info('app.jsx - Wiping localStorage due to new username existing');
  Cookies.set('username', window.dfs.user.username);
  window.localStorage.removeItem('redux');
}

// set new version
window.localStorage.setItem('version', window.dfs.gitCommitUUID);

// Registration
require('components/account/register');

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
require('components/account/user_limits');

// Lobby
require('components/nav-scoreboard/nav-scoreboard');
require('components/lobby/lobby-container');
require('components/lobby/lobby-lineup-card-list');

// Draft
require('components/draft/draft-lineup-card-list');
require('components/draft/draft-sport-title');
require('components/draft/draft-container');

// Live
require('components/live/live');

// Results
require('components/results/results');

// Live modal
require('components/modal/live-modal');
