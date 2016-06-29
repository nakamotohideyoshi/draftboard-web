import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveMLBPitchZonePitch from '../../../../components/live/mlb/live-mlb-pitch-zone-pitch.jsx';


/**
 * Tests for LiveMLBPitchZone
 */
describe('<LiveMLBPitchZonePitch /> Component', () => {
  const renderComponent = (props) => mount(<LiveMLBPitchZonePitch {...props} />);

  const defaultTestProps = {
    count: 3,
    left: 10,
    outcome: 'strike',
    speed: 92,
    top: 10,
    type: 'FA',
    zone: 12,
  };

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render an li', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('li')).to.have.length(1);
  });

  it('should render out modifiers correctly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find(
      'li.live-mlb-pitch-zone-pitch.live-mlb-pitch-zone-pitch--strike.live-mlb-pitch-zone-pitch--zone-12'
    )).to.have.length(1);
  });

  it('should render props properly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.live-mlb-pitch-zone-pitch__count').text()).to.equal('3');
    expect(wrapper.find('.live-mlb-pitch-zone-pitch__speed').text()).to.equal('92 MPH');
    expect(wrapper.find('.live-mlb-pitch-zone-pitch__type').text()).to.equal('FA');
  });
});
