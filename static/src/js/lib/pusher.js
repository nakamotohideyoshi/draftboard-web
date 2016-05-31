/**
 * include and instantiate a new Pusher object with either test stub data or a
 * legit Pusher connection based on the NODE_ENV.
 */
import log from './logging.js';

let Pusher;

if (process.env.NODE_ENV === 'test') {
  log.info('Importing PusherTestStub');
  Pusher = require('./pusher-test-stub/PusherTestStub');
} else {
  log.info('Connecting to Pusher');
  Pusher = require('pusher-js');
}

export default new Pusher(window.dfs.user.pusher_key, {
  encrypted: true,
});
