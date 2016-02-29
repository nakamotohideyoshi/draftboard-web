/**
 * Responsible for creating the system's store with all the desired
 * reducers and middlewares. The store is a singleton used all across
 * the system.
 */

import persistState from 'redux-localstorage';
import { compose } from 'redux';

import createStoreWithMiddleware from './middleware/index';
import reducers from './reducers/index';

const liveSubstates = [
  'currentLineups',
  'entries',
  'liveContests',
  'liveDraftGroups',
  'livePlayers',
  'prizes',
];

/**
 * Method called each time redux state is saved, and saves `subset` to localStorage
 * @param  {object} ) Redux state
 * @return {object}   Object to store to localStorage
 */
const slicer = () => (state) => {
  const subset = {};

  // save sports when available
  if (state.sports.games !== {}) {
    subset.sports = state.sports;
  }

  // only store entries and related info once all loaded
  if (state.entries.hasRelatedInfo === true) {
    liveSubstates.forEach((subState) => subset[subState] = state[subState]);
  }

  return subset;
};

const createPersistentStore = compose(
  persistState([], { slicer })
)(createStoreWithMiddleware);

// Store WITH localStorage, is default
export default createPersistentStore(reducers);

// Store WITHOUT localStorage, turn on if you need to debug
// export default middleware.createStoreWithMiddleware(reducers)
