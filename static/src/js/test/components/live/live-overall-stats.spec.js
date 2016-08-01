import React from 'react';
import merge from 'lodash/merge';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveOverallStats from '../../../components/live/live-overall-stats.jsx';
import Odometer from '../../../components/site/odometer.jsx';


/**
 * Tests for LiveOverallStats
 * - not able to test canvas, svg at the moment
 */
describe('<LiveOverallStats /> Component', () => {
  const renderComponent = (props) => mount(<LiveOverallStats {...props} />);

  const defaultTestProps = {
    fp: 20.33333,
    id: 2,
    name: 'My Lineup',
    potentialWinnings: 2.123123,
    rank: 40,
    timeRemaining: {
      decimal: 0.5,
      duration: 153,
    },
    whichSide: 'mine',
  };

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render section', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.live-overall-stats')).to.have.length(1);
  });

  it('should render stats strings correctly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.live-overall-stats__name').text()).to.equal('My Lineup');
    expect(wrapper.find('.live-overall-stats__rank').text()).to.equal('40th /');
    expect(wrapper.find('.live-overall-stats__amount').text()).to.equal('$2.12');
    expect(wrapper.find(Odometer)).to.have.length(1);
    expect(wrapper.find('.live-overall-stats__duration').text()).to.equal('153');
  });

  it('should render villian stats strings correctly', () => {
    const props = merge({}, defaultTestProps, { id: 1 });
    const wrapper = renderComponent(props);

    expect(wrapper.find('.live-overall-stats__rank').text()).to.equal('');
    expect(wrapper.find('.live-overall-stats__amount').text()).to.equal('N/A');
  });
});
