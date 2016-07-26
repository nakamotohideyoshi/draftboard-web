import assert from 'assert';
import nock from 'nock';

import * as actions from '../../../actions/user/register';


describe('actions.user.register', () => {
  before(() => {
    nock.disableNetConnect();
  });

  after(() => {
    nock.enableNetConnect();
  });

  afterEach(() => {
    nock.cleanAll();
  });

  it('should correctly POST registerUser', () => {
    nock('http://localhost')
      .post('/api/account/register/', {
        username: 'user',
        email: 'user@test.com',
        password: 'password',
        password_confirm: 'password',
      })
      .reply(201, {});

    actions.registerUser(
      'user@test.com',
      'username',
      'password',
      'password'
    ).then(response => {
      assert.equal(response, true);
    });
  });

  it('should correctly error out registerUser', () => {
    nock('http://localhost')
      .post('/api/account/register/', {
        username: 'user',
        password: 'password',
        password_confirm: 'password',
      })
      .reply(400, {
        json: {
          email: ['Required field'],
        },
      });

    actions.registerUser(
      'user@test.com',
      'username',
      'password',
      'password'
    ).catch(errors => {
      assert.equal(errors.email[0], 'Required field');
    });
  });
});
