import log from 'loglevel';
import createLogger from 'redux-logger';


/**
 * Return the appropriate log level
 * @return {string} The log level
 */
const getLevel = () => {
  // Default to errors only and prouction
  let logLevel = 'error';

  if (process.env.NODE_ENV === 'debug' || process.env.NODE_ENV === 'development') {
    logLevel = 'debug';
  }

  if (process.env.NODE_ENV === 'test') {
    logLevel = 'warn';
  }

  // override with URL query param
  if (window.dfs.logLevel !== '') {
    logLevel = window.dfs.logLevel;
  }

  return logLevel;
};

// get and set the appropriate logging level
export const logLevel = getLevel();
log.setLevel(logLevel);

// by default, export the log object to work with
export default log;

// configure redux-logging, is added in to middleware
// TODO: remove || logLevel === 'error' to disable redux-logger on staging/production.
export const logger = createLogger({
  predicate: () => logLevel === 'debug' || logLevel === 'error',
  collapsed: true,
});
