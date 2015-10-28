"use strict";

/**
 *   Responsible for creating the system's store with all the desired
 * reducers and middlewares. The store is a singleton used all across
 * the system.
 */

const reducers = require('./reducers');
const middleware = require('./middleware');

module.exports = middleware.createStoreWithMiddleware(reducers);
