import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import NavScoreboardSlider from '../../../components/nav-scoreboard/nav-scoreboard-slider.jsx';
import NavScoreboardSeparator from '../../../components/nav-scoreboard/nav-scoreboard-separator.jsx';

// TODO: Find a way to test scrolling. Currently JSDOM doesn't support
//       advanced DOM properties used in the component.

describe('NavScoreboardSlider Component', () => {
  const renderComponent = (props) => mount(<NavScoreboardSlider {...props} />);

  it('should not render if no children', () => {
    const wrapper = renderComponent({});
    expect(wrapper.find(NavScoreboardSeparator)).to.have.length(0);
  });

  it('should render with children', () => {
    const props = {
      children: ['<div />'],
    };

    const wrapper = renderComponent(props);
    expect(wrapper.find('.cmp-nav-scoreboard--slider')).to.have.length(1);
    expect(wrapper.find('.slider-content.not-scrollable')).to.have.length(1);
  });
});
