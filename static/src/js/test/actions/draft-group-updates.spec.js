import { assert } from 'chai';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';

import * as actionTypes from '../../action-types';
import * as actions from '../../actions/draft-group-updates';
import draftGroupUpdatesReducer from '../../reducers/draft-group-updates';
import sportUpdatesFix from '../../fixtures/json/sport-updates';
import find from 'lodash/find';


describe('actions.draftGroupUpdates.fetchDraftGroupUpdates', () => {
  let store = {};

  before(() => {
    nock.disableNetConnect();
  });

  beforeEach(() => {
    // initial store, state
    store = mockStore({
      draftGroupUpdates: draftGroupUpdatesReducer(undefined, {}),
    });
  });


  after(() => {
    nock.enableNetConnect();
  });


  afterEach(() => {
    nock.cleanAll();
  });


  it('should fetch contest pool entries', () => {
    nock('http://localhost')
      .get('/api/sports/player-status/nfl/')
      .reply(200, sportUpdatesFix);

    return store.dispatch(actions.fetchDraftGroupUpdates('nfl'))
      .then(() => {
        const dispatchedActions = store.getActions();
        // Did the action get dispatched?
        assert.isDefined(find(dispatchedActions, { type: 'DRAFT_GROUP_UPDATES__FETCHING' }));

        const actionBody = find(
          dispatchedActions,
          { type: 'DRAFT_GROUP_UPDATES__FETCH_SUCCESS' }
        ).response;
        // Is the content payload of the action correct?
        // Because the data gets normalized in the action, do some basic checks.
        // assert.equal(Object.keys(actionBody).length, sportUpdatesFix.length);
        assert.equal(actionBody.sport, 'nfl');
        assert.property(actionBody, 'updates');
        assert.property(actionBody.updates, 'gameUpdates');
        assert.property(actionBody.updates, 'playerUpdates');
        // the fixtures have 2 injury updates for 2 differnet playres, these get grouped, so we
        // should have 2 injury update entries.
        assert.equal(Object.keys(actionBody.updates.playerUpdates.injury).length, 2);
      });
  });


  it('should fail properly.', () => {
    nock('http://localhost')
      .get('/api/sports/updates/nfl/')
      .reply(400, { detail: 'something is wrong.' });

    return store.dispatch(actions.fetchDraftGroupUpdates('nfl'))
      .then(() => {
        assert.isDefined(
          find(store.getActions(), { type: actionTypes.DRAFT_GROUP_UPDATES__FETCH_FAIL }),
          'When fetch fails, the fail action is not being dispatched'
        );
      });
  });
});
