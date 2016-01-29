/**
 * Responsible for creating the system's store with all the desired
 * reducers and middlewares. The store is a singleton used all across
 * the system.
 */

import persistState from 'redux-localstorage';
import { compose } from 'redux';

import createStoreWithMiddleware from './middleware/index';
import reducers from './reducers/index';

const createPersistentStore = compose(
  persistState([
    'currentDraftGroups',
    'currentLineups',
    'entries',
    'liveContests',
    'liveDraftGroups',
    'livePlayers',
    'playerBoxScoreHistory',
    'prizes',
    'sports',
  ])
)(createStoreWithMiddleware);

// Store WITH localStorage, is default
export default createPersistentStore(reducers);

// Store WITHOUT localStorage, turn on if you need to debug
// export default middleware.createStoreWithMiddleware(reducers)
