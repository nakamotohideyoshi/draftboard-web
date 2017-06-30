import { assert } from 'chai';
import mockStore from '../mock-store-with-middleware';
import nock from 'nock';

// import * as actionTypes from '../../action-types';
import * as actions from '../../actions/user';
// import find from 'lodash/find';


describe('actions.user.verifyLocation', () => {
  let store = {};

  before(() => {
    nock.disableNetConnect();
  });

  beforeEach(() => {
    // initial store, state
    store = mockStore({});
  });

  after(() => {
    nock.enableNetConnect();
  });

  afterEach(() => {
    nock.cleanAll();
  });

  // it('should redirect on 403 response', () => {
  //   nock('http://localhost')
  //     .get('/api/account/verify-location/')
  //     .reply('403', { detail: 'IP_CHECK_FAILED' });
  //
  //   return store.dispatch(actions.verifyLocation()).then((res) => {
  //     assert.equal(res.error, 'redirecting due to location restriction.');
  //   });
  // });

  it('should not error on a 200 response', () => {
    nock('http://localhost')
      .get('/api/account/verify-location/')
      .reply('200', { detail: 'location verification passed' });

    return store.dispatch(actions.verifyLocation()).then((res) => {
      assert.isUndefined(res.error);
    });
  });
});
