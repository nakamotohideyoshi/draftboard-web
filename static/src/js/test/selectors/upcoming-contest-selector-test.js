import { expect } from 'chai';
import { upcomingContestSelector } from '../../selectors/upcoming-contest-selector.js';
import * as contestFixtures from '../../fixtures/json/store-upcoming-contests.js';
import store from '../../store.js';


describe('UpcomingContestSelector', () => {
  let appState = {};

  beforeEach(() => {
    // Let all of the reducers create the default, empty store and then duplicate it so we can
    // mutate it for testing purposes.
    appState = Object.assign({}, store.getState());
  });


  it('should return empty array when no contest are present.', () => {
    expect(upcomingContestSelector(appState)).to.be.an('array');
    expect(upcomingContestSelector(appState)).to.have.lengthOf(0);
  });


  it('should return all contest when no filters are set.', () => {
    // Populate the store with our store fixture data.
    appState.upcomingContests.allContests = contestFixtures.allContests;
    expect(upcomingContestSelector(appState)).to.be.an('array');
    expect(upcomingContestSelector(appState)).to.have.lengthOf(Object.keys(contestFixtures.allContests).length);
  });


  // it('should filter based on a contest name', () => {
  //
  // });
});
