import braintree from 'braintree-web';
import { fetchPayPalClientTokenIfNeeded } from '../../actions/payments';
import store from '../../store';
import log from '../logging';
import actionTypes from '../../action-types';
import { addMessage } from '../../actions/message-actions';


/**
 * Use the braintree library to setup a paypal button.
 * Once it is ready, onPaymentMethodReceived will be called.
 *
 * @param  {[type]} id                       =             'paypal-container'              [description]
 * @param  {[type]} amount                   the dollar amount of the transaction
 * @param  {[type]} onCancelled              =             onCancelledDefault              [description]
 * @param  {[type]} onReady                  =             onReadyDefault                  [description]
 * @param  {[type]} onUnsupported            =             onUnsupportedDefault            [description]
 * @param  {[type]} onAuthorizationDismissed =             onAuthorizationDismissedDefault [description]
 * @return {[type]}                          [description]
 */
export const setupPaypalButton = (
  id = 'paypal-container',
  amount,
  onReady = () => {log.info('no onReady callback provided.');},
  onCancelled = () => {log.info('no onCancelled callback provided.');},
  onUnsupported = () => {log.info('no onUnsupported callback provided.');},
  onAuthorizationDismissed = () => {log.info('no onAuthorizationDismissed callback provided.');},
  onPaymentMethodReceived = () => {log.info('no onPaymentMethodReceived callback provided.');}
) => {
  log.info('Initializing Braintree...');

  // Default callback actions to take.
  //
  // We have a set of default actions that do some default things, as well as invoking any
  // passed-in callback functions.
  const onReadyDefault = (integration) => {
    log.info('Paypal integration ready.', integration);
    onReady(integration);
  };

  const onCancelledDefault = () => {
    log.warn('paypal checkout was cancelled by user.');

    store.dispatch({
      type: actionTypes.PAYPAL_CANCELLED,
    });

    store.dispatch(addMessage({
      header: 'Deposit Cancelled',
      level: 'warning',
      content: 'No funds have been deposited. Sign into PayPal again to proceed.',
      id: 'paypalCancelledByUser',
    }));

    onCancelled();
  };

  const onUnsupportedDefault = () => {
    log.warn('paypal checkout was cancelled due to an unsupported browser.');

    store.dispatch(addMessage({
      header: 'Browser Unsupported',
      level: 'warning',
      content: 'Your browser is not supported by PayPal.',
    }));

    onUnsupported();
  };

  const onAuthorizationDismissedDefault = () => {
    log.info('paypal checkout popup was closed.');
    onAuthorizationDismissed();
  };

  const onPaymentMethodReceivedDefault = (obj) => {
    log.info('onPaymentMethodReceived response:', obj);

    store.dispatch({
      type: actionTypes.PAYPAL_NONCE_RECEIVED,
      nonce: obj.nonce,
    });

    onPaymentMethodReceived(obj);
  };


  // Setup the darn button already!
  return store.dispatch(
  // If we don't have a client token already (we likely do), fetch one.
    fetchPayPalClientTokenIfNeeded())
    // Once we have a client token, we can use the braintree sdk to add a button
    // to the DOM id we provided.
    .then(() => {
      log.info('Client token obtained, setting up braintree checkout.');
      const appState = store.getState();
      log.info(`Setting up Paypal button for $${amount}`);

      // Do braintree's setup stuff.
      braintree.setup(appState.payments.payPalClientToken, 'custom', {
        // Paypal checkout options:
        // https://developers.braintreepayments.com/reference/client-reference/javascript/v2/paypal#options
        paypal: {
          // headless: true,
          container: id,
          singleUse: true,
          intent: 'authorize',
          submit_for_settlement: true,
          amount,
          currency: 'USD',
          locale: 'en_us',
          enableShippingAddress: false,
          enableBillingAddress: false,
          onCancelled: () => onCancelledDefault(),
          onUnsupported: () => onUnsupportedDefault(),
          onAuthorizationDismissed: () => onAuthorizationDismissedDefault(),
        },
        onPaymentMethodReceived: (obj) => onPaymentMethodReceivedDefault(obj),
        onReady: (integration) => onReadyDefault(integration),
      });
    }
  );
};
