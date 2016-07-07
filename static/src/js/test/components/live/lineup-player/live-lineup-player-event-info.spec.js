import merge from 'lodash/merge';
import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveLineupPlayerEventInfo from '../../../../components/live/lineup-player/live-lineup-player-event-info.jsx';


/**
 * Tests for LiveMLBPitchZone
 */
describe('<LiveLineupPlayerEventInfo /> Component', () => {
  const renderComponent = (props) => mount(<LiveLineupPlayerEventInfo {...props} />);

  const defaultTestProps = {
    info: 'Someone did something',
    points: 10,
    when: '5:32',
  };

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render a div', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.live-lineup-player-event-info')).to.have.length(1);
  });

  it('should not render points if they do not exist', () => {
    const newProps = merge({}, defaultTestProps);
    delete(newProps.points);

    const wrapper = renderComponent(newProps);

    expect(wrapper.find('.live-lineup-player-event-info__points')).to.have.length(0);
  });

  it('should render props properly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.live-lineup-player-event-info__points').text()).to.equal('+10');
    expect(wrapper.find('.live-lineup-player-event-info__info').text()).to.equal(defaultTestProps.info);
    expect(wrapper.find('.live-lineup-player-event-info__when').text()).to.equal(defaultTestProps.when);
  });
});
