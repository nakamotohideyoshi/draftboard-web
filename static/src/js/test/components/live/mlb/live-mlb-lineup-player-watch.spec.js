import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveMLBDiamond from '../../../../components/live/mlb/live-mlb-diamond.jsx';
import LiveMlbLineupPlayerWatch from '../../../../components/live/mlb/live-mlb-lineup-player-watch.jsx';


/**
 * Tests for LiveMlbLineupPlayerWatch
 */
describe('<LiveMlbLineupPlayerWatch /> Component', () => {
  const renderComponent = (props) => mount(<LiveMlbLineupPlayerWatch {...props} />);

  const defaultTestProps = {
    modifiers: ['active'],
    multipartEvent: {
      pitchCount: 3,
      pitcher: {
        outcomeFp: 3.2,
      },
      runners: [],
      when: {
        half: 't',
        inning: '8th',
      },
    },
    onClick: () => 'onClick worked',
    player: {
      id: 2,
      name: 'Foo Bar',
      type: 'pitcher',
    },
  };

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render a div', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.live-mlb-lineup-player-watch')).to.have.length(1);
  });

  it('should render out modifiers correctly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find(
      'div.live-mlb-lineup-player-watch.live-mlb-lineup-player-watch--active'
    )).to.have.length(1);
  });

  it('should render properly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.live-mlb-lineup-player-watch__fp').text()).to.equal('3.2');
    expect(wrapper.find('.live-mlb-lineup-player-watch__name').text()).to.equal('Foo Bar');
    expect(wrapper.find('.live-mlb-lineup-player-watch__pitch-count').text()).to.equal('3');
    expect(wrapper.find('.live-mlb-lineup-player-watch__inning-str').text()).to.equal('8th');

    expect(wrapper.find(LiveMLBDiamond)).to.have.length(1);
  });
});
