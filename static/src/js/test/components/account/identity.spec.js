import React from 'react';
import { assert } from 'chai';
import { mount } from 'enzyme';
import Component from '../../../components/account/subcomponents/identity';


/**
 * Tests for Deposit form.
 */
describe('<Identity /> Component', () => {
  const renderComponent = (props) => mount(<Component {...props} />);
  const defaultTestProps = {
    identity: {},
  };
  let wrapper = null;


  afterEach(() => {
    document.body.innerHTML = '';
  });


  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render a div', () => {
    assert.lengthOf(wrapper.find('.cmp-account-identity'), 1);
  });


  it('should display info when an identity is available', () => {
    wrapper.setProps({
      identity: {
        first_name: 'steve',
        last_name: 'steve-last',
      },
    });

    assert.lengthOf(wrapper.find('.username-display'), 1);
  });

  //
  //
  // it('should default to a disabled paypal button', () => {
  //   assert.isTrue(
  //     wrapper.ref('paypal-button').prop('disabled'),
  //     'Paypal button is not disabled by default.'
  //   );
  // });
  //
  //
  // it('should enable paypal button only if no nonce, amount and !isDepositing are present', () => {
  //   // starts off disabled.
  //   assert.isTrue(
  //     wrapper.ref('paypal-button').prop('disabled'),
  //     'Paypal button is wrongly enabled.'
  //   );
  //
  //   // add an amount
  //   wrapper.setState({ amount: 25 });
  //   assert.isFalse(
  //     wrapper.ref('paypal-button').prop('disabled'),
  //     'Paypal button is not enabling.'
  //   );
  //
  //   // pretend a deposit is happening.
  //   wrapper.setProps({ isDepositing: true });
  //   assert.isTrue(
  //     wrapper.ref('paypal-button').prop('disabled'),
  //     'Paypal button not disabling when a deposit is taking place.'
  //   );
  //
  //   // Should disable if a nonce is present
  //   wrapper.setProps({ payPalNonce: 'we have a nonce :)' });
  //   assert.isTrue(
  //     wrapper.ref('paypal-button').prop('disabled'),
  //     'Paypal button is wrongly enabled. If we have recieved a nonce, it should be disabled.'
  //   );
  // });
});
