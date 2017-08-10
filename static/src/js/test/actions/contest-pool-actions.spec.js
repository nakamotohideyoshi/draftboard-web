import { assert } from 'chai';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';

import * as actionTypes from '../../action-types';
import * as actions from '../../actions/contest-pool-actions';
import contestPoolEntriesReducer from '../../reducers/contest-pool-entries';
const userReducer = require('../../reducers/user');
import contestPoolsReducer from '../../reducers/contest-pools';
import contestPoolEntriesFix from '../../fixtures/json/contest--current-entries';
import contestPoolFix from '../../fixtures/json/contest-pools';
import find from 'lodash/find';

import merge from 'lodash/merge';


describe('actions.contestPoolActions.fetchContestPoolEntries', () => {
  let store = {};

  before(() => {
    nock.disableNetConnect();
  });

  beforeEach(() => {
    // initial store, state
    store = mockStore({
      contestPoolEntries: contestPoolEntriesReducer(undefined, {}),
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
      .get('/api/contest/contest-pools/entries/')
      .reply(200, contestPoolEntriesFix);

    return store.dispatch(actions.fetchContestPoolEntries())
      .then(() => {
        const dispatchedActions = store.getActions();
        // Did the action get dispatched?
        assert.isDefined(find(dispatchedActions, { type: 'FETCHING_CONTEST_POOL_ENTRIES' }));

        const actionBody = find(
          dispatchedActions,
          { type: 'FETCH_CONTEST_POOL_ENTRIES_SUCCESS' }
        ).response;
        // Is the content payload of the action correct?
        // Because the data gets normalized in the action, just check that the count of elements is
        // correct.
        assert.equal(Object.keys(actionBody).length, contestPoolEntriesFix.length);
      });
  });


  it('should fail properly.', () => {
    nock('http://localhost')
      .get('/api/contest/contest-pools/entries/')
      .reply(400, { detail: 'something is wrong.' });

    return store.dispatch(actions.fetchContestPoolEntries())
      .then(() => {
        assert.isDefined(
          find(store.getActions(), { type: actionTypes.FETCH_CONTEST_POOL_ENTRIES_FAIL }),
          'When fetch fails, the fail action is not being dispatched'
        );
      });
  });
});


describe('actions.contestPoolActions.setFocusedContest', () => {
  let store = {};

  beforeEach(() => {
    // initial store, state
    store = mockStore({
      contestPools: contestPoolsReducer(undefined, {}),
    });
  });

  it('should create an action.', () => {
    store.dispatch(actions.setFocusedContest(666));
    assert.isDefined(
      find(store.getActions(), { type: actionTypes.SET_FOCUSED_CONTEST, contestId: 666 }),
      'setFocusedContest thunk is not dispatching the correct action.'
    );
  });
});


describe('actions.contestPoolActions.fetchContestPools', () => {
  let store = {};

  before(() => {
    nock.disableNetConnect();
  });

  beforeEach(() => {
    // initial store, state
    store = mockStore({
      contestPools: contestPoolsReducer(undefined, {}),
    });
  });


  after(() => {
    nock.enableNetConnect();
  });


  afterEach(() => {
    nock.cleanAll();
  });


  it('should fetch contest pools', () => {
    nock('http://localhost')
      .get('/api/contest/lobby/')
      .reply(200, contestPoolFix);

    return store.dispatch(actions.fetchContestPools())
      .then(() => {
        const dispatchedActions = store.getActions();
        // Did the action get dispatched?
        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FETCH_CONTEST_POOLS }),
          'correct action not dispatched'
        );

        const actionBody = find(
          dispatchedActions,
          { type: actionTypes.FETCH_CONTEST_POOLS_SUCCESS }
        ).response;

        // Is the content payload of the action correct?
        // Because the data gets normalized in the action, just check that the count of elements is
        // correct.
        assert.equal(Object.keys(actionBody).length, contestPoolFix.length);
      });
  });


  it('should fail properly.', () => {
    nock('http://localhost')
      .get('/api/contest/lobby/')
      .reply(400, { detail: 'something is wrong.' });

    return store.dispatch(actions.fetchContestPools())
      .then(() => {
        assert.isDefined(
          find(store.getActions(), { type: actionTypes.FETCH_CONTEST_POOLS_FAIL }),
          'When fetch fails, the fail action is not being dispatched'
        );
      });
  });
});


describe('actions.contestPoolActions.updateFilter', () => {
  let store = {};

  beforeEach(() => {
    // initial store, state
    store = mockStore();
  });

  it('should create an action.', () => {
    const filter = {
      filterName: 'name',
      filterProperty: 'prop',
      match: 'match',
    };

    store.dispatch(actions.updateFilter(filter.filterName, filter.filterProperty, filter.match));

    assert.isDefined(
      find(store.getActions(), { type: actionTypes.UPCOMING_CONTESTS_FILTER_CHANGED, filter }),
      'updateFilter thunk is not dispatching the correct action.'
    );
  });
});


describe('actions.contestPoolActions.updateOrderByFilter', () => {
  let store = {};

  beforeEach(() => {
    // initial store, state
    store = mockStore();
  });

  it('should create an action.', () => {
    const orderBy = {
      property: 'prop',
      direction: 'dir',
    };

    store.dispatch(actions.updateOrderByFilter(orderBy.property, orderBy.direction));

    assert.isDefined(
      find(store.getActions(), { type: actionTypes.UPCOMING_CONTESTS_ORDER_CHANGED, orderBy }),
      'updateOrderByFilter thunk is not dispatching the correct action.'
    );
  });
});


describe('actions.contestPoolActions.enterContest', () => {
  let store = {};

  before(() => {
    nock.disableNetConnect();
  });

  beforeEach(() => {
    const verifiedUserState = merge(
      {},
      userReducer(undefined, {}),
      { user: { identity_verified: true } }
    );
    // initial store, state
    store = mockStore({
      contestPoolEntries: contestPoolEntriesReducer(undefined, {}),
      user: userReducer(verifiedUserState, {}),
      contestPools: contestPoolsReducer(undefined, {}),
    });
  });


  after(() => {
    nock.enableNetConnect();
  });


  afterEach(() => {
    nock.cleanAll();
  });


  it('should enter a contest', () => {
    const contestPoolId = 666;
    const lineupId = 111;

    // mock enter-lineup endpoint
    nock('http://localhost')
      .post('/api/contest/enter-lineup/')
      .reply(200, { status: 'SUCCESS' })
      // mock entries endpoint
      .get('/api/contest/contest-pools/entries/')
      .reply(200, contestPoolEntriesFix)
      // mock the lobby
      .get('/api/contest/lobby/')
      .reply(200, contestPoolFix);

    return store.dispatch(actions.enterContest(contestPoolId, lineupId))
      .then(() => {
        const dispatchedActions = store.getActions();
        // Did the action get dispatched?
        assert.isDefined(
          find(dispatchedActions, {
            type: actionTypes.ENTERING_CONTEST_POOL,
            contestPoolId,
            lineupId,
          }), 'entering action not dispatched'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FETCHING_CASH_BALANCE }),
          'after entering contest, balance is not fetched'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FETCH_CONTEST_POOLS }),
          'after entering contest, contest pools are not fetched'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.ADD_MESSAGE }),
          'after entering contest, message is not shown'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FETCHING_CONTEST_POOL_ENTRIES }),
          'after entering contest, entries are not fetched'
        );

        assert.isDefined(find(
          dispatchedActions, {
            type: actionTypes.ENTERING_CONTEST_POOL_SUCCESS,
            contestPoolId,
            lineupId,
          }), 'success action not dispatched'
        );
      });
  });


  it('should fail properly.', () => {
    const contestPoolId = 666;
    const lineupId = 111;

    // mock entries endpoint
    nock('http://localhost')
      .get('/api/contest/contest-pools/entries/')
      .reply(200, contestPoolEntriesFix)
      // mock the lobby
      .get('/api/contest/lobby/')
      .reply(200, contestPoolFix)
      // mock enter-lineup endpoint failure
      .post('/api/contest/enter-lineup/')
      .reply(400, { detail: 'this should fail and log - contest-pool-actions.spec' });

    return store.dispatch(actions.enterContest(contestPoolId, lineupId))
      .then(() => {
        const dispatchedActions = store.getActions();

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.ENTERING_CONTEST_POOL_FAIL }),
          'When fetch fails, the fail action is not being dispatched'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FETCH_CONTEST_POOLS }),
          'after entering contest, contest pools are not fetched'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.ADD_MESSAGE }),
          'after entering contest, message is not shown'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FETCHING_CONTEST_POOL_ENTRIES }),
          'after entering contest, entries are not fetched'
        );
      });
  });
});


// describe('actions.contestPoolActions.fetchContestEntrants', () => {

// });


describe('actions.contestPoolActions.upcomingContestUpdateReceived', () => {
  let store = {};

  beforeEach(() => {
    store = mockStore();
  });

  it('should create an action.', () => {
    const contest = {
      id: 666,
    };

    store.dispatch(actions.upcomingContestUpdateReceived(contest));

    assert.isDefined(
      find(store.getActions(), { type: actionTypes.UPCOMING_CONTESTS_UPDATE_RECEIVED, contest }),
      'upcomingContestUpdateReceived thunk is not dispatching the correct action.'
    );
  });
});


describe('actions.contestPoolActions.removeContestPoolEntry', () => {
  let store = {};

  before(() => {
    nock.disableNetConnect();
  });

  beforeEach(() => {
    // initial store, state
    store = mockStore({
      contestPoolEntries: contestPoolEntriesReducer(undefined, {}),
      user: userReducer(undefined, {}),
      contestPools: contestPoolsReducer(undefined, {}),
    });
  });


  after(() => {
    nock.enableNetConnect();
  });


  afterEach(() => {
    nock.cleanAll();
  });


  it('should deregister from a contest', () => {
    const entry = {
      id: 666,
    };

    // mock enter-lineup endpoint
    nock('http://localhost')
      .post(`/api/contest/unregister-entry/${entry.id}/`)
      .reply(200, { status: 'SUCCESS' })
      // mock entries endpoint
      .get('/api/contest/contest-pools/entries/')
      .reply(200, contestPoolEntriesFix)
      // mock the lobby
      .get('/api/contest/lobby/')
      .reply(200, contestPoolFix);

    return store.dispatch(actions.removeContestPoolEntry(entry))
      .then(() => {
        const dispatchedActions = store.getActions();
        // Did the action get dispatched?
        assert.isDefined(
          find(dispatchedActions, {
            type: actionTypes.REMOVING_CONTEST_POOL_ENTRY,
            entry,
          }), 'deregistering action not dispatched'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FETCHING_CASH_BALANCE }),
          'after entering contest, balance is not fetched'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FETCH_CONTEST_POOLS }),
          'after entering contest, contest pools are not fetched'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.ADD_MESSAGE }),
          'after entering contest, message is not shown'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FETCHING_CONTEST_POOL_ENTRIES }),
          'after entering contest, entries are not fetched'
        );

        assert.isDefined(find(
          dispatchedActions, {
            type: actionTypes.REMOVING_CONTEST_POOL_ENTRY_SUCCESS,
            entry,
          }), 'success action not dispatched'
        );
      });
  });


  it('should fail properly.', () => {
    const entry = {
      id: 666,
    };

    // mock entries endpoint
    nock('http://localhost')
      .get('/api/contest/contest-pools/entries/')
      .reply(200, contestPoolEntriesFix)
      // mock the lobby
      .get('/api/contest/lobby/')
      .reply(200, contestPoolFix)
      // mock enter-lineup endpoint failure
      .post(`/api/contest/unregister-entry/${entry.id}/`)
      .reply(400, { detail: 'this should fail and log - contest-pool-actions.spec' });

    return store.dispatch(actions.removeContestPoolEntry(entry))
      .then(() => {
        const dispatchedActions = store.getActions();

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.REMOVING_CONTEST_POOL_ENTRY_FAIL, entry }),
          'When fetch fails, the fail action is not being dispatched'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FETCH_CONTEST_POOLS }),
          'after entering contest, contest pools are not fetched'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.ADD_MESSAGE }),
          'after entering contest, message is not shown'
        );

        assert.isDefined(
          find(dispatchedActions, { type: actionTypes.FETCHING_CONTEST_POOL_ENTRIES }),
          'after entering contest, entries are not fetched'
        );
      });
  });
});
