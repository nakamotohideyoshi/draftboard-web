import log from 'loglevel';
import createLogger from 'redux-logger';


/**
 * Returns a default logging level based on environment
 *
 * @return {String} [description]
 */
const getDefaultLevel = () => {
  const { NODE_ENV } = process.env;

  // sometimes it's called development so map to debug
  if (['debug', 'development'].indexOf(NODE_ENV) > -1) return 'DEBUG';

  // increase level for testing in cloud, we don't want to see bc we're already testing
  if (NODE_ENV === 'test') return 'WARN';

  // default to errors only for production
  return 'ERROR';
};

// Is our environment set to test? We use this so redux logger actions are hidden
// when running tests.
const isTestingEnv = process.env.NODE_ENV === 'test';

// default if setLevel isn't used, see
// https://www.npmjs.com/package/loglevel for more info
log.setDefaultLevel(getDefaultLevel());

// setLevel if user overrides

if (
  window.dfs &&
  window.dfs.logLevel &&
  ['trace', 'debug', 'info', 'warn', 'error'].indexOf(window.dfs.logLevel) > -1
) {
  const { logLevel } = window.dfs;

  // let the user know what they did
  const overrideLog = log.getLogger('override-log-level');
  overrideLog.setLevel('WARN');
  overrideLog.warn(`Log level overridden by backend, set to "${logLevel}"`);

  // don't persist! we do that in python so we can clear js localStorage yet still log
  log.setLevel(logLevel, false);
  log.getLogger('action').setLevel(logLevel);
  log.getLogger('app').setLevel(logLevel);  // normally DEBUG
  log.getLogger('app-state-store').setLevel(logLevel);
  log.getLogger('component').setLevel(logLevel);
  log.getLogger('lib').setLevel(logLevel);
  log.getLogger('selector').setLevel(logLevel);
} else {
  // default custom loggers to production level, change when debugging locally
  // search for `getLogger` on this page to learn more https://www.npmjs.com/package/loglevel
  log.getLogger('action').setLevel('SILENT');
  log.getLogger('app').setLevel('DEBUG');  // normally DEBUG
  log.getLogger('app-state-store').setLevel('SILENT');
  log.getLogger('component').setLevel('SILENT');
  log.getLogger('lib').setLevel('SILENT');
  log.getLogger('selector').setLevel('SILENT');
}


// by default, export the log object to work with
export default log;

// we export this to have test to ensure this is never shown on production
// works differently than setLevel, shows for any level less than this reduxLoggerLevel
// default to TRACE so it does not show
export const reduxLoggerLevel = log.levels.TRACE;

// configure redux-logging to show messages about reducer state
// show for TRACE, DEBUG, INFO, WARN levels
export const logger = createLogger({
  predicate: () => !isTestingEnv,
  collapsed: true,
});

// give access to the logger so you can make more granular after load
// example, write in console: logging.log.getLogger('action').setLevel('SILENT')
window.logging = {
  log,
};
