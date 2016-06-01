/**
 * include and instantiate a new Pusher object with either test stub data or a
 * legit Pusher connection based on the NODE_ENV.
 */
import log from './logging.js';
import { addMessage, removeMessage } from '../actions/message-actions.js';
import store from '../store';
import Pusher from 'pusher-js';


log.info('Connecting to Pusher');

const pusher = new Pusher(window.dfs.user.pusher_key, {
  encrypted: true,
});


/**
 * Attach a handful of hooks to display status messages to the user.
 * Docs: https://pusher.com/docs/client_api_guide/client_connect#connection_states
 */


/**
 * The connection is temporarily unavailable.
 * Pusher will automatically retry the connection every ten seconds.
 */
pusher.connection.bind('unavailable', () => {
  store.dispatch(addMessage({
    header: 'Cannot connect to live update server.',
    content: 'This is likely temporary and the connection will be retried.',
    id: 'pusherLog',
  }));
});

/**
 * The Pusher connection was previously connected and has now intentionally been closed.
 */
pusher.connection.bind('disconnected', () => {
  store.dispatch(addMessage({
    header: 'Live update server has been disconnected.',
    content: 'Please refresh the page to reconnect.',
    id: 'pusherLog',
  }));
});

/**
 * Pusher is not supported by the browser.
 */
pusher.connection.bind('failed', () => {
  store.dispatch(addMessage({
    header: 'Live update server connection has failed.',
    content: 'it appears that your browser unsupported.',
    id: 'pusherLog',
  }));
});

/**
 *	The connection to Pusher is open and authenticated with your app.
 */
pusher.connection.bind('connected', () => {
  // Clear any pusher messages.
  store.dispatch(removeMessage('pusherLog'));
});


export default pusher;
