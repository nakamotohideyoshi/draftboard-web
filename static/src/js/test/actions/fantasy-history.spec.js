import { assert } from 'chai';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';

import * as actionTypes from '../../action-types';
import * as actions from '../../actions/fantasy-history-actions';
import fantasyHistoryReducer from '../../reducers/fantasy-history';
import fantasyHistoryFix from '../../fixtures/json/fantasy-history';
import find from 'lodash/find';


describe('actions.fantasyHistory.fetchFantasyHistory', () => {
  let store = {};

  before(() => {
    nock.disableNetConnect();
  });

  beforeEach(() => {
    // initial store, state
    store = mockStore({
      fantasyHistory: fantasyHistoryReducer(undefined, {}),
    });
  });


  after(() => {
    nock.enableNetConnect();
  });


  afterEach(() => {
    nock.cleanAll();
  });


  it('should fetch fantasy history', () => {
    nock('http://localhost')
      .get('/api/sports/fp-history/nfl/')
      .reply(200, fantasyHistoryFix);


    return store.dispatch(actions.fetchFantasyHistory('nfl'))
      .then(() => {
        const dispatchedActions = store.getActions();
        // Did the action get dispatched?
        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FANTASY_HISTORY__FETCH_SUCCESS }),
          'Success action was not dispatched'
        );

        const actionBody = find(
          dispatchedActions,
          { type: actionTypes.FANTASY_HISTORY__FETCH_SUCCESS }
        ).response;

        // Is the content payload of the action correct?
        // Because the data gets normalized in the action, do some basic checks.
        // should have the same number of entries as the fixture.
        assert.equal(Object.keys(actionBody).length, fantasyHistoryFix.length);
      });
  });


  it('should fail properly.', () => {
    nock('http://localhost')
      .get('/api/sports/fp-history/nfl/')
      .reply(400, { detail: 'something is wrong.' });

    return store.dispatch(actions.fetchFantasyHistory('nfl'))
      .then(() => {
        assert.isDefined(
          find(store.getActions(), { type: actionTypes.FANTASY_HISTORY__FETCH_FAIL }),
          'When fetch fails, the fail action is not being dispatched'
        );
      });
  });
});
