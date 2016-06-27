import { expect } from 'chai';
import { contestPoolsSelector } from '../../selectors/contest-pools-selector.js';
import * as contestFixtures from '../../fixtures/json/store-upcoming-contests.js';
import store from '../../store.js';


describe('contestPoolselector', () => {
  let appState = {};

  beforeEach(() => {
    // Let all of the reducers create the default, empty store and then duplicate it so we can
    // mutate it for testing purposes.
    appState = Object.assign({}, store.getState());
  });


  it('should return empty array when no contest are present.', () => {
    expect(contestPoolsSelector(appState)).to.be.an('array');
    expect(contestPoolsSelector(appState)).to.have.lengthOf(0);
  });


  it('should return all contest when no filters are set.', () => {
    // Populate the store with our store fixture data.
    appState.contestPools.allContests = contestFixtures.allContests;
    // Reset the default sport filter.
    appState.contestPools.filters.sportFilter.match = '';
    expect(contestPoolsSelector(appState)).to.be.an('array');
    // This is no longer true because we are
    expect(contestPoolsSelector(appState)).to.have.lengthOf(Object.keys(contestFixtures.allContests).length);
  });
});
