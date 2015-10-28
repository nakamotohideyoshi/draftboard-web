"use strict";

/**
 *   Responsible for combining all the system's middlewares in a
 * single place.
 */

const { createStore, applyMiddleware } = require('redux');

const createLogger = require('redux-logger');
const thunkMiddleware = require('redux-thunk');


const loggerMiddleware = createLogger();


exports.createStoreWithMiddleware = applyMiddleware(
  thunkMiddleware, // lets us #dispatch() functions
  loggerMiddleware // neat middleware that logs actions in the console
)(createStore);
