import React from 'react';
import { assert } from 'chai';
import { mount } from 'enzyme';
import Component from '../../../components/account/withdrawals';
import PubSub from 'pubsub-js';


const defaultTestProps = {
  errors: {},
  isWithdrawing: false,
  onWithdraw: () => true,
  verifyLocation: () => true,
  fetchUser: () => true,
  gidxWithdrawForm: {
    formEmbed: ''
  },
};


describe('<Withdrawals /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<Component {...props} />);
  }


  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  afterEach(() => {
    document.body.innerHTML = '';
  });


  it('renders the withdrawals component.', () => {
    assert.lengthOf(wrapper.find('.cmp-account-withdrawals'), 1);
    assert.lengthOf(wrapper.find(Component), 1);
  });


  it('renders 2 form fields.', () => {
    assert.lengthOf(wrapper.find('input[name="amount"]'), 1);
  });


  // it('displays errors.', () => {
  //   // add some amount errors.
  //   wrapper.setProps({
  //     errors: {
  //       amount: ['first error', 'second'],
  //     },
  //   });
  //
  //   assert.lengthOf(wrapper.find('.form-field-message__description'), 2);
  //
  //   // Add an email error.
  //   wrapper.setProps({
  //     errors: {
  //       amount: wrapper.props().errors.amount,
  //       email: ['first error'],
  //     },
  //   });
  //
  //   assert.lengthOf(wrapper.find('.form-field-message__description'), 3);
  // });

  
  // it('disables the submit button when a request is pending.', () => {
  //   assert.notInclude(wrapper.ref('submit').node.className, 'button--disabled');
  //   wrapper.setProps({ isWithdrawing: true });
  //   assert.include(wrapper.ref('submit').node.className, 'button--disabled');
  // });
});
