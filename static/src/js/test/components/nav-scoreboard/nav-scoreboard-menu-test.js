'use strict';

import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import NavScoreboardMenu from "../../../components/nav-scoreboard/nav-scoreboard-menu.jsx";

describe('NavScoreboardMenu Component', function() {

  function renderComponent() {
    return mount(<NavScoreboardMenu />);
  }

  it('should render', function() {
    const wrapper = renderComponent();
    expect(wrapper.find('.cmp-nav-scoreboard--menu')).to.have.length(1);
  });

  it("should toogle on click", function() {
    const wrapper = renderComponent();
    expect(wrapper.find('.mobile-forum-hamburger.closed')).to.have.length(0);

    wrapper.find('.mobile-forum-hamburger').simulate('click');
    expect(wrapper.find('.mobile-forum-hamburger.closed')).to.have.length(1);

    wrapper.find('.mobile-forum-hamburger').simulate('click');
    expect(wrapper.find('.mobile-forum-hamburger.closed')).to.have.length(0);
  });
});
