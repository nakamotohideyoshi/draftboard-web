import log from 'loglevel';
import createLogger from 'redux-logger';


/**
 * Returns a default logging level based on environment
 *
 * @return {[type]} [description]
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

// default if setLevel isn't used, see
// https://www.npmjs.com/package/loglevel for more info
log.setDefaultLevel(getDefaultLevel());

// setLevel if user overrides
if (['trace', 'debug', 'info', 'warn', 'error'].indexOf(window.dfs.logLevel) > -1) {
  const { logLevel } = window.dfs;

  // let the user know what they did
  const overrideLog = log.getLogger('override-log-level');
  overrideLog.setLevel('WARN');
  overrideLog.warn(`Log level overridden by backend, set to "${logLevel}"`);

  // don't persist! we do that in python so we can clear js localStorage yet still log
  log.setLevel(logLevel, false);
}

// default custom loggers to production level, change when debugging locally
// search for `getLogger` on this page to learn more https://www.npmjs.com/package/loglevel
log.getLogger('action').setLevel('SILENT');
log.getLogger('app').setLevel('DEBUG');  // normally DEBUG
log.getLogger('app-state-store').setLevel('SILENT');
log.getLogger('component').setLevel('SILENT');
log.getLogger('selector').setLevel('SILENT');

// by default, export the log object to work with
export default log;

// we export this to have test to ensure this is never shown on production
// works differently than setLevel, shows for any level less than this reduxLoggerLevel
// default to TRACE so it does not show
export const reduxLoggerLevel = log.levels.TRACE;

// configure redux-logging to show messages about reducer state
// show for TRACE, DEBUG, INFO, WARN levels
export const logger = createLogger({
  predicate: () => log.getLevel() < reduxLoggerLevel,
  collapsed: true,
});
