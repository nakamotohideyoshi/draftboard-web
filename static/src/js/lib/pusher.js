// middleman to allow use of the test stub when testing
// unfortunate, but they don't support commonjs yet https://github.com/pusher-community/pusher-js-test-stub/issues/19
// and pusher themselves recommend using the test stub

import Pusher from 'pusher-js';
import PusherTestStub from './pusher-test-stub/PusherTestStub';

let SetPusher = Pusher;

if (process.env.NODE_ENV === 'test') {
  SetPusher = PusherTestStub;
}

export default SetPusher;
