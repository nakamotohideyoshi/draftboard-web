/**
 * Responsible for creating the system's store with all the desired
 * reducers and middlewares. The store is a singleton used all across
 * the system.
 */

import persistState from 'redux-localstorage';
import { compose } from 'redux';
import { enableBatching } from 'redux-batched-actions';

import createStoreWithMiddleware from './middleware/index';
import reducers from './reducers/index';

const liveSubstates = [
  // Disable caching of these as they are goofing with results section stuff.
  // 'currentLineups',
  // 'liveContests',
  'liveDraftGroups',
  'livePlayers',
  'prizes',
];

/**
 * Method called each time redux state is saved, and saves `subset` to localStorage
 * @return {object}   Object to store to localStorage
 */
const slicer = () => (state) => {
  const subset = {};

  if (state.version !== {}) {
    subset.version = state.version;
  }

  // save sports when available
  if (state.sports.games !== {}) {
    subset.sports = state.sports;
  }

  // only store entries and related info once all loaded
  if (state.currentLineups.hasRelatedInfo === true) {
    liveSubstates.forEach((subState) => (subset[subState] = state[subState]));
  }

  return subset;
};

const createPersistentStore = compose(
  persistState([], { slicer })
)(createStoreWithMiddleware);

// Store WITH localStorage, is default
export default createPersistentStore(enableBatching(reducers));

// Store WITHOUT localStorage, turn on if you need to debug
// export default middleware.createStoreWithMiddleware(reducers)
