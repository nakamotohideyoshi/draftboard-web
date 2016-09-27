import React from 'react';
// import sinon from 'sinon';
import { expect } from 'chai';
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
  };


  afterEach(() => {
    document.body.innerHTML = '';
  });


  it('should render a div', () => {
    const wrapper = renderComponent(defaultTestProps);
    expect(wrapper.find('.cmp-account-deposits')).to.have.length(1);
  });
});
