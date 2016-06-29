import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveMLBStadium from '../../../../components/live/mlb/live-mlb-stadium.jsx';
import LiveMLBPitchZone from '../../../../components/live/mlb/live-mlb-pitch-zone.jsx';


/**
 * Tests for LiveMLBPitchZone
 */
describe('<LiveMLBStadium /> Component', () => {
  const renderComponent = (props) => mount(<LiveMLBStadium {...props} />);

  const defaultTestProps = {
    event: {
      hitter: {
        atBatStats: '1 for 3, 2B',
        name: 'Foo Bar',
      },
      zonePitches: [{
        count: 3,
        left: 10,
        outcome: 'strike',
        speed: 92,
        top: 10,
        type: 'FA',
        zone: 12,
      }],
    },
    modifiers: ['all-mine'],
    whichSide: 'mine',
  };

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render a section', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('section')).to.have.length(1);
  });

  it('should render out modifiers correctly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find(
      '.live-mlb-stadium.live-mlb-stadium--all-mine'
    )).to.have.length(1);
  });

  it('should render pitch zone properly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find(LiveMLBPitchZone)).to.have.length('1');
  });

  it('should render props properly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.live-mlb-stadium__hitter-record').text()).to.equal('1 for 3, 2B');
    expect(wrapper.find('.live-mlb-stadium__hitter-name').text()).to.equal('Foo Bar');
  });
});
