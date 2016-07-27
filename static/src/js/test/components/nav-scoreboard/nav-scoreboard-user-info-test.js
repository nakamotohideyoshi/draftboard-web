'use strict';

import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import NavScoreboardUserInfo from '../../../components/nav-scoreboard/nav-scoreboard-user-info.jsx';

const defaultProps = {
  name: 'John',
  cashBalance: {
    amount: 100,
  },
};

describe('NavScoreboardUserInfo Component', function () {

  function renderComponent() {
    return mount(<NavScoreboardUserInfo
                   name={defaultProps.name}
                   balance={defaultProps.cashBalance.amount} />);
  }

  it('should render a div tag, name and balance', function () {
    const wrapper = renderComponent();
    expect(wrapper.find('.name')).to.have.length(1);
    expect(wrapper.find('.name').text()).to.equal(defaultProps.name);
    expect(wrapper.find('.balance')).to.have.length(1);
    expect(wrapper.find('.balance').text())
      .to.contain(`$${defaultProps.cashBalance.amount}.00`);
  });
});
