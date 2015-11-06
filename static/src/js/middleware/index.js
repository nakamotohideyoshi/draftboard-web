"use strict";

import createLogger from 'redux-logger';
import { createStore, applyMiddleware } from 'redux';
import { logLevel } from '../config';
import { thunkMiddleware } from 'redux-thunk';


// only show redux actions logs in development mode
const loggerMiddleware = createLogger({
  predicate: (getState, action) => logLevel === 'debug'
});


/**
 * Responsible for combining all the system's middlewares in a single place.
 */
exports.createStoreWithMiddleware = applyMiddleware(
  thunkMiddleware, // lets us #dispatch() functions
  loggerMiddleware // neat middleware that logs actions in the console
)(createStore);
