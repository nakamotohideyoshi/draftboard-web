import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';

import { Register } from '../../../components/account/register.jsx';


/**
 * Tests for Register
 */
describe('<Register /> Component', () => {
  const renderComponent = (props) => mount(<Register {...props} />);

  const defaultTestProps = {
    actions: {
      registerUser: sinon.spy(),
    },
    verifyLocation: sinon.spy(),
    userLocation: {
      status: 'unknown',
      isLocationVerified: false,
      isSending: false,
      hasAttemptedToVerify: false,
      message: null,
    },
  };

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render a div', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.account__left__content__form')).to.have.length(1);
  });

  // it('should set error on terms when empty form is submitted', () => {
  //   const wrapper = renderComponent(defaultTestProps);
  //
  //   wrapper.find('input[type="submit"]').first().simulate('click', () => {
  //     expect(wrapper.find('account__left__content__form__input-layout__terms.errored')).to.have.length(1);
  //   });
  //
  //   // expect(defaultTestProps.actions.registerUser.calledWith()).to.equal(true);
  // });
  //
  // it('should run registerUser when form is submitted', () => {
  //   const wrapper = renderComponent(defaultTestProps);
  //
  //   wrapper.find('input[name="terms"]').first().simulate('click', () => {
  //     wrapper.find('input[type="submit"]').first().simulate('click', () => {
  //       expect(wrapper.find('account__left__content__form__input-layout__terms.errored')).to.have.length(1);
  //       expect(defaultTestProps.actions.registerUser.callCount()).to.equal(1);
  //     });
  //   });
  // });
});
