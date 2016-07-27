'use strict';

import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import NavScoreboardSlider from "../../../components/nav-scoreboard/nav-scoreboard-slider.jsx";

// TODO: Find a way to test scrolling. Currently JSDOM doesn't support
//       advanced DOM properties used in the component.

describe('NavScoreboardSlider Component', function() {

  function renderComponent() {
    return mount(<NavScoreboardSlider />);
  }

  it('should render', function() {
    const wrapper = renderComponent();
    expect(wrapper.find('.cmp-nav-scoreboard--slider')).to.have.length(1);
    expect(wrapper.find('.slider-content.not-scrollable')).to.have.length(1);
  });
});
