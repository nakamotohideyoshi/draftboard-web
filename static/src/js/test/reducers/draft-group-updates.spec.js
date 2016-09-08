import { assert } from 'chai';
import reducer from '../../reducers/draft-group-updates';
import * as actionTypes from '../../action-types';
import draftGroupUpdatesData from '../../fixtures/json/action-output/draft-group-updates';


describe('reducers.draft-group-updates', () => {
  const defaultState = reducer(undefined, {});


  it('should return the initial state', () => {
    assert.equal('nba' in defaultState.sports, true);
    assert.equal('nfl' in defaultState.sports, true);
    assert.equal('mlb' in defaultState.sports, true);
    assert.equal('nhl' in defaultState.sports, true);
    assert.deepEqual(defaultState.sports.nba, {});
    assert.deepEqual(defaultState.sports.nfl, {});
    assert.deepEqual(defaultState.sports.mlb, {});
    assert.deepEqual(defaultState.sports.nhl, {});
    assert.typeOf(defaultState.isFetching, 'object');
  });


  it('should return state if invalid action type used', () => {
    const newState = reducer(defaultState, { type: 'nonexistent' });
    assert.deepEqual(defaultState, newState);
  });


  it('should handle DRAFT_GROUP_UPDATES__FETCHING', () => {
    const state = reducer(defaultState, {
      type: actionTypes.DRAFT_GROUP_UPDATES__FETCHING,
      sport: 'nba',
    });

    assert.equal(state.isFetching.nba, true);
    assert.equal(state.isFetching.nfl, false);
    assert.equal(state.isFetching.mlb, false);
    assert.equal(state.isFetching.nhl, false);
  });


  it('should handle DRAFT_GROUP_UPDATES__FETCH_FAIL', () => {
    // have isFetching set to true
    let state = reducer(defaultState, {
      type: actionTypes.DRAFT_GROUP_UPDATES__FETCHING,
      sport: 'nba',
    });
    assert.equal(state.isFetching.nba, true);

    // then test it goes back to false.
    state = reducer(state, {
      type: actionTypes.DRAFT_GROUP_UPDATES__FETCH_FAIL,
      sport: 'nba',
    });
    assert.equal(state.isFetching.nba, false);
  });


  it('should handle DRAFT_GROUP_UPDATES__FETCH_SUCCESS', () => {
    // set fetching flag to true, then make sure it gets flipped.
    defaultState.isFetching[draftGroupUpdatesData.sport] = true;
    const state = reducer(defaultState, {
      type: actionTypes.DRAFT_GROUP_UPDATES__FETCH_SUCCESS,
      response: draftGroupUpdatesData,
    });
    assert.isFalse(state.isFetching[draftGroupUpdatesData.sport]);

    assert.deepEqual(
      state.sports[draftGroupUpdatesData.sport].playerUpdates,
      draftGroupUpdatesData.updates.playerUpdates
    );

    assert.deepEqual(
      state.sports[draftGroupUpdatesData.sport].gameUpdates,
      draftGroupUpdatesData.updates.gameUpdates
    );
  });
});
