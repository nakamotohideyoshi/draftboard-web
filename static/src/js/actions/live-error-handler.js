import log from '../lib/logging';
import Raven from 'raven-js';
import { addMessage } from './message-actions.js';


export default (exception, message) => (dispatch) => {
  Raven.captureException(exception);

  dispatch(addMessage(message));

  // show for development purposes
  log.error(exception);
};
