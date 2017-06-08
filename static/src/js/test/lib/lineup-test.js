/* eslint-disable no-param-reassign */
import { assert } from 'chai';
import * as lineup from '../../lib/lineup.js';
import newLineup from '../../fixtures/json/create-new-lineup.js';

// rosterTemplates
describe('lib.lineup.rosterTemplates', () => {
  it('should contain a roster template for each sport', () => {
    assert.isTrue('nfl' in lineup.rosterTemplates, 'NFL roster template exists');
    assert.isTrue('nba' in lineup.rosterTemplates, 'NBA roster template exists');
    assert.isTrue('nhl' in lineup.rosterTemplates, 'NHL roster template exists');
    assert.isTrue('mlb' in lineup.rosterTemplates, 'MLB roster template exists');
  });


  it('should contain the correct number of slots each sport', () => {
    assert.equal(lineup.rosterTemplates.nfl.length, 8, 'NFL player count');
    assert.equal(lineup.rosterTemplates.nba.length, 8, 'NBA player count');
    assert.equal(lineup.rosterTemplates.nhl.length, 8, 'NHL player count');
    assert.equal(lineup.rosterTemplates.mlb.length, 9, 'MLB player count');
  });
});


// salaryCaps
describe('lib.lineup.salaryCaps', () => {
  it('should contain a cap for each sport', () => {
    assert.isTrue('nfl' in lineup.salaryCaps, 'NFL salaryCap exists');
    assert.isTrue('nba' in lineup.salaryCaps, 'NBA salaryCap exists');
    assert.isTrue('nhl' in lineup.salaryCaps, 'NHL salaryCap exists');
    assert.isTrue('mlb' in lineup.salaryCaps, 'MLB salaryCap exists');
  });
});


// validateLineup
describe('lib.lineup.validateLineup', () => {
  it('should throw an error when lineup is incomplete', () => {
    // copy the array.
    const lineupMissingPlayer = newLineup.slice();
    // remove a player.
    lineupMissingPlayer[2] = {};
    const errors = lineup.validateLineup(lineupMissingPlayer);
    assert.equal(errors[0], 'lineup is not completely filled.', 'all slots are filled.');
    assert.equal(errors.length, 1, 'throws only 1 error');
  });


  // salary validation is done in the reducer.
  // it('should trow an error if over salary cap', () => {
  //   // copy the array.
  //   const lineupOverBudget = newLineup.slice();
  //   lineupOverBudget[0].player.salary = 9999999999999;
  //   const errors = lineup.validateLineup(lineupOverBudget);
  //   assert.equal(errors[0], 'lineup is not completely filled.', 'all slots are filled.');
  //   assert.equal(errors.length, 1, 'throws only 1 error');
  // });
});
