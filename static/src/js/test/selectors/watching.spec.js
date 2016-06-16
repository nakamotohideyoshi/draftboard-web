import { assert } from 'chai';
import {
  isLoadingObj,
  watchingMyLineupSelector,
} from '../../selectors/watching';

import output3 from '../../fixtures/json/selectors-output/live/3.json';
import state1 from '../../fixtures/json/redux-state/live/1.json';
import state2 from '../../fixtures/json/redux-state/live/2.json';
import state3 from '../../fixtures/json/redux-state/live/3.json';


// default lineup info
export const testLineup = {
  id: 5,
  name: 'Ultimate',
  roster: [200],
  draftGroup: 52,
};

// note how we don't need to test every situation of data coming in because we already did with compileLineupStats
describe('selectors.watchingMyLineupSelector', () => {
  it('should return loading object if a user has not chosen a lineup yet', () => {
    assert.deepEqual(watchingMyLineupSelector(state1), isLoadingObj);
  });

  it('should return loading object if client has not received currentLineups yet', () => {
    assert.deepEqual(watchingMyLineupSelector(state2), isLoadingObj);
  });

  it('should return full object otherwise', () => {
    assert.deepEqual(watchingMyLineupSelector(state3), output3);
  });
});
