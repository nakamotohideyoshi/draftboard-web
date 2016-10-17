import Raven from 'raven-js';
import braintree from 'braintree-web';
import { fetchPayPalClientTokenIfNeeded } from '../../actions/payments';
import store from '../../store';
import log from '../logging';
import actionTypes from '../../action-types';
import { addMessage } from '../../actions/message-actions';
import merge from 'lodash/merge';


/**
 * Use the braintree library to setup a paypal button.
 * Once it is ready, onPaymentMethodReceived will be called.
 * The following params are passed through as a single `args` object, then
 * merged with a default set.
 *
 * @param  {Object} paypalButton = DOM elment of the PayPal button.
 * @param  {Int} amount = the dollar amount of the transaction.
 * @param  {Function} onClosed = Callback for when the user closes the popup.
 * @param  {Function} onReady = Callback for when the button is initialized.
 * @param  {Function} onError = Callback for when an error has occurred.
 * @param  {Function} onPaymentMethodReceived = Callback for when a nonce is received.
 * @return {Promise}
 */
export function beginPaypalCheckout(args = {}) {
  // Default set of callback arguments.
  const defaultArgs = {
    onReady: (integration) => {
      log.info('PayPal ready.', integration);
    },
    onPaymentMethodReceived: (obj) => {
      log.info('onPaymentMethodReceived response:', obj);
    },
    onError: (err) => {
      Raven.captureException(err);
      log.error(err);
      // Show error banner to user.
      return store.dispatch(addMessage({
        level: 'warning',
        header: 'Deposit Failed',
        content: err.details,
      }));
    },
    onClosed: (err) => {
      log.info('paypal done.', err);
    },
  };


  // Merge the provided and defaults.
  const options = merge({}, defaultArgs, args);
  log.info(`Fetching a nonce for $${options.amount}`);

  // Because tokenization opens a popup, this has to be called as a result of
  // customer action, like clicking a button—you cannot call this at any time.
  options.paypalInstance.tokenize({
    flow: 'checkout', // Required
    amount: options.amount, // Required
    currency: 'USD', // Required
    locale: 'en_US',
    enableShippingAddress: false,
    intent: 'authorize',
    shippingAddressEditable: false,
  }, (tokenizeErr, payload) => {
    // Stop if there was an error.
    if (tokenizeErr) {
      switch (tokenizeErr.code) {
        case 'PAYPAL_POPUP_CLOSED':
          log.info('PayPal popup closed.', tokenizeErr);
          options.onClosed();
          break;
        default:
          options.onError(tokenizeErr);
          options.onClosed();
      }
      return;
    }

    // Tokenization succeeded!
    // Send tokenizationPayload.nonce to server
    options.onPaymentMethodReceived(payload.nonce, options.amount);
    // Dispatch an action to save the nonce in our datastore.
    return store.dispatch({
      type: actionTypes.PAYPAL_NONCE_RECEIVED,
      nonce: payload.nonce,
    });
  });
}


export const setupBraintree = (callback) => {
  log.info('Initializing Braintree...');

  // Set up the button!
  return store.dispatch(
    // If we don't have a client token already (we likely do), fetch one.
    fetchPayPalClientTokenIfNeeded())
    // Once we have a client token, we can use the braintree sdk to add a button
    // to the DOM id we provided.
    .then(() => {
      log.info('Client token obtained, setting up braintree checkout.');
      const appState = store.getState();

      // Create a Client component
      braintree.client.create({
        authorization: appState.payments.payPalClientToken,
      }, (clientErr, clientInstance) => {
        // Stop if there was a problem creating the client.
        // This could happen if there is a network error or if the authorization
        // is invalid.
        if (clientErr) {
          // Capture the error and display a user message.
          Raven.captureException(clientErr);
          return store.dispatch(addMessage({
            level: 'warning',
            header: 'PayPal Initiation Failed',
            content: clientErr,
          }));
        }

        // Create PayPal component
        braintree.paypal.create({
          client: clientInstance,
        }, (paypalErr, paypalInstance) => {
          // Stop if there was a problem creating PayPal.
          // This could happen if there was a network error or if it's incorrectly
          // configured.
          if (paypalErr) {
            log.error('Error creating PayPal:', paypalErr);

            return;
          }

          // Let the dispatcher know that the button is ready.
          callback(paypalInstance);
        });
      });
    }
  );
};
