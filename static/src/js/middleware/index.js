const createStore = require('redux').createStore
const applyMiddleware = require('redux').applyMiddleware
const createLogger =  require('redux-logger')
const logLevel = require('../config').logLevel
const thunkMiddleware = require('redux-thunk')


// only show redux actions logs in development mode
const loggerMiddleware = createLogger({
  predicate: () => logLevel === 'debug'
});


/**
 * Responsible for combining all the system's middlewares in a single place.
 */
exports.createStoreWithMiddleware = applyMiddleware(
  thunkMiddleware, // lets us #dispatch() functions
  loggerMiddleware // neat middleware that logs actions in the console
)(createStore);
