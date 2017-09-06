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
    identityFormInfo: {},
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
    gidxPaymentForm: {},
    fetchDepositForm: () => true,
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
});
