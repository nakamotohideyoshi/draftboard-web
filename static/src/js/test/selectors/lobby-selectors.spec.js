/* eslint-disable quote-props */
import { assert } from 'chai';
import { entrySkillLevelsSelector } from '../../selectors/lobby-selectors';
import store from '../../store.js';
import merge from 'lodash/merge';


describe('selectors.LobbySelectors.entrySkillLevelsSelector', () => {
  // Stripped down example entries.
  const entries = {
    10: { contest_pool: 1, sport: 'mlb' },
    11: { contest_pool: 1, sport: 'mlb' },
    20: { contest_pool: 12, sport: 'nfl' },
  };

  // Stripped down example contests.
  const contests = {
    // MLB
    1: { 'sport': 'mlb', 'skill_level': { 'name': 'rookie' } },
    2: { 'sport': 'mlb', 'skill_level': { 'name': 'veteran' } },
    3: { 'sport': 'mlb', 'skill_level': { 'name': 'veteran' } },
    4: { 'sport': 'mlb', 'skill_level': { 'name': 'all' } },
    // NFL
    11: { 'sport': 'nfl', 'skill_level': { 'name': 'rookie' } },
    12: { 'sport': 'nfl', 'skill_level': { 'name': 'veteran' } },
    13: { 'sport': 'nfl', 'skill_level': { 'name': 'veteran' } },
    14: { 'sport': 'nfl', 'skill_level': { 'name': 'all' } },
  };

  let appState = {};

  beforeEach(() => {
    // Let all of the reducers create the default, empty store and then duplicate it so we can
    // mutate it for testing purposes.
    appState = merge({}, store.getState());
  });

  afterEach(() => {
    appState = {};
  });

  it('should return empty object when no data is present.', () => {
    assert.typeOf(entrySkillLevelsSelector(appState), 'object');
    assert.lengthOf(Object.keys(entrySkillLevelsSelector(appState)), 0);
  });


  it('should return an object when data is present.', () => {
    // Populate the store with our store fixture data.
    appState.contestPools.allContests = contests;
    appState.contestPoolEntries.entries = entries;
    assert.typeOf(entrySkillLevelsSelector(appState), 'object');
  });


  it('should have an element for each sport the user is entered into.', () => {
    // Populate the store with our store fixture data.
    appState.contestPools.allContests = contests;
    appState.contestPoolEntries.entries = entries;
    const output = entrySkillLevelsSelector(appState);
    // Should have an entry for each sport
    assert.lengthOf(Object.keys(output), 2);
    assert.isTrue('mlb' in output);
    assert.isTrue('nfl' in output);
    assert.isFalse('nba' in output);
    assert.isFalse('nhl' in output);
  });


  it('should attach the correct skill level for each contest entry', () => {
    appState.contestPools.allContests = contests;
    appState.contestPoolEntries.entries = entries;
    const output = entrySkillLevelsSelector(appState);
    assert.equal(output.nfl, 'veteran');
    assert.equal(output.mlb, 'rookie');
  });


  it('should ignore the \'all\' skill level.', () => {
    appState.contestPools.allContests = contests;
    // Assign this entry to an 'all' contest.
    appState.contestPoolEntries.entries = { 10: { contest_pool: 4, sport: 'mlb' } };
    const output = entrySkillLevelsSelector(appState);
    assert.isUndefined(output.mlb, 'all skill level is not being ignored.');
  });
});
