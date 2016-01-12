"use strict";

/**
 *   Responsible for creating the system's store with all the desired
 * reducers and middlewares. The store is a singleton used all across
 * the system.
 */

const reducers = require('./reducers');
const middleware = require('./middleware');
import log from './lib/logging'

// before we load the store, wipe redux if asked
if (window.dfs.wipeRedux === "1") {
    log.debug('store.js - Wiping localStorage')
    window.localStorage.clear()
}

// Store with localStorage, commented out until we have Pusher installed and working on optimizations
import {compose, createStore} from 'redux';
import persistState from 'redux-localstorage'
const createPersistentStore = compose(
  persistState([
    'currentBoxScores',
    'currentDraftGroups',
    'currentLineups',
    'entries',
    'liveContests',
    'liveDraftGroups',
    'prizes',
    'sports'
  ])
)(middleware.createStoreWithMiddleware)
module.exports = createPersistentStore(reducers)

// module.exports = middleware.createStoreWithMiddleware(reducers)