import braintree from 'braintree-web';
import { fetchPayPalClientToken } from '../../actions/payments.js';
import store from '../../store';
import log from '../logging.js';
import actionTypes from '../../action-types.js';


// First get a client token from our server
export const setupOnDomElementId = (id = 'paypal-container') => store.dispatch(
  fetchPayPalClientToken()).then(() => {
    const appState = store.getState();
    log.info('token recieved, setting up braintree.');
    // then do braintree's setup stuff.
    return braintree.setup(appState.payments.payPalClientToken, 'custom', {
      paypal: {
        container: id,
        singleUse: true,
        amount: 1.00,
        currency: 'USD',
        enableShippingAddress: false,
      },
      onPaymentMethodReceived: (obj) => {
        store.dispatch({
          type: actionTypes.PAYPAL_NONCE_RECEIVED,
          nonce: obj.nonce,
        });
        // doSomethingWithTheNonce(obj.nonce);
      },
    });
  }
);
