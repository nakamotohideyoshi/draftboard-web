import React from 'react';
// import sinon from 'sinon';
import { assert } from 'chai';
import { mount } from 'enzyme';
import Deposits from '../../../components/account/deposits';


/**
 * Tests for Deposit form.
 */
describe('<Deposits /> Component', () => {
  const renderComponent = (props) => mount(<Deposits {...props} />);
  const defaultTestProps = {
    user: {},
    deposit: () => true,
    isDepositing: false,
    payPalNonce: null,
    payPalClientToken: null,
    setupBraintree: () => true,
    beginPaypalCheckout: () => true,
    verifyLocation: () => true,
    verifyIdentity: () => true,
    fetchUser: () => true,
    userLocation: {},
    checkUserIdentityVerificationStatus: () => true,
    gidxFormInfo: {},
  };
  let wrapper = null;

  afterEach(() => {
    document.body.innerHTML = '';
  });

  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render a div', () => {
    assert.lengthOf(wrapper.find('.cmp-account-deposits'), 1);
  });


  it('should default to a disabled paypal button', () => {
    assert.isTrue(
      wrapper.ref('paypal-button').prop('disabled'),
      'Paypal button is not disabled by default.'
    );
  });


  it('should enable paypal button only if no nonce, amount and !isDepositing are present', () => {
    // starts off disabled.
    assert.isTrue(
      wrapper.ref('paypal-button').prop('disabled'),
      'Paypal button is wrongly enabled.'
    );

    // add an amount
    wrapper.setState({ amount: 25 });
    assert.isFalse(
      wrapper.ref('paypal-button').prop('disabled'),
      'Paypal button is not enabling.'
    );

    // pretend a deposit is happening.
    wrapper.setProps({ isDepositing: true });
    assert.isTrue(
      wrapper.ref('paypal-button').prop('disabled'),
      'Paypal button not disabling when a deposit is taking place.'
    );

    // Should disable if a nonce is present
    wrapper.setProps({ payPalNonce: 'we have a nonce :)' });
    assert.isTrue(
      wrapper.ref('paypal-button').prop('disabled'),
      'Paypal button is wrongly enabled. If we have recieved a nonce, it should be disabled.'
    );
  });
});
