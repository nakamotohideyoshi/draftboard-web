import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveMLBPitchZone from '../../../../components/live/mlb/live-mlb-pitch-zone.jsx';
import LiveMLBPitchZonePitch from '../../../../components/live/mlb/live-mlb-pitch-zone-pitch.jsx';


/**
 * Tests for LiveMLBPitchZone
 */
describe('<LiveMLBPitchZone /> Component', () => {
  const renderComponent = (props) => mount(<LiveMLBPitchZone {...props} />);

  const defaultTestProps = {
    modifiers: ['mine'],
    zonePitches: [{
      count: 3,
      left: 10,
      outcome: 'strike',
      speed: 92,
      top: 10,
      type: 'FA',
      zone: 12,
    }],
  };

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render a div', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.live-mlb-pitch-zone')).to.have.length(1);
  });

  it('should render out modifiers correctly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find(
      'div.live-mlb-pitch-zone.live-mlb-pitch-zone--mine'
    )).to.have.length(1);
  });

  it('should not render pitches if they do not exist', () => {
    const props = {
      modifiers: ['mine'],
      // no zonePitches!
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('ul.live-mlb-pitch-zone__pitches')).to.have.length('0');
  });

  it('should render pitches properly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find(LiveMLBPitchZonePitch)).to.have.length('1');
  });
});
