"use strict";

/**
 *   Responsible for creating the system's store with all the desired
 * reducers and middlewares. The store is a singleton used all across
 * the system.
 */

const reducers = require('./reducers');
const middleware = require('./middleware');

// Store with localStorage, commented out until we have Pusher installed and working on optimizations
// import {compose, createStore} from 'redux';
// import persistState from 'redux-localstorage'
// const createPersistentStore = compose(
//   persistState([
//     'currentLineups',
//     'entries',
//     'liveContests',
//     'liveDraftGroups',
//     'prizes'
//   ])
// )(middleware.createStoreWithMiddleware)
// module.exports = createPersistentStore(reducers)

module.exports = middleware.createStoreWithMiddleware(reducers)