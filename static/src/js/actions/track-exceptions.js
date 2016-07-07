import log from '../lib/logging';
import Raven from 'raven-js';
import { addMessage } from './message-actions.js';


/**
 * Wrapper to capture exceptions that break stuff
 * Sends information to Raven and console, as well as shows message to user
 * @param  {object} extra   Anything relevant to the message we might want to know
 * @param  {string} message What happened?
 */
export const handleError = (exception, message) => (dispatch) => {
  Raven.captureException(exception);

  dispatch(addMessage(message));

  // show for development purposes
  log.error(exception);
};

/**
 * Wrapper to capture unexpected things that don't necessarily break functionality
 * Sends information to Raven and console
 *
 * https://docs.getsentry.com/hosted/clients/javascript/usage/#passing-additional-data
 *
 * @param  {object} extra   Anything relevant to the message we might want to know
 * @param  {string} message What happened?
 *
 * @return {boolean}  Always return false so that we can return this function
 */
export const trackUnexpected = (message, extra) => {
  // wrap extra in an object bc Sentry expects extra property
  Raven.captureMessage(message, {
    extra,
    level: 'info',
  });

  // show for development purposes
  log.info(message, extra);

  return false;
};
