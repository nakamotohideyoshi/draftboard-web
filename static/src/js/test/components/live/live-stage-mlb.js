import merge from 'lodash/merge';
import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveMLBStage from '../../../components/live/live-stage-mlb.jsx';
import LiveMLBStadium from '../../../components/live/mlb/live-mlb-stadium.jsx';


/**
 * Tests for LiveMLBStage
 */
describe('<LiveMLBStage /> Component', () => {
  const renderComponent = (props) => mount(<LiveMLBStage {...props} />);

  const defaultTestProps = {
    currentEvent: null,
    eventsMultipart: {
      events: [],
      watchablePlayers: [],
    },
    watching: {
      myLineupId: 2,
      sport: 'mlb',
    },
  };

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render a div', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.live__venue-mlb')).to.have.length(1);
  });

  it('should render out single MLB stadium if only watching my MLB lineup', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find(LiveMLBStadium)).to.have.length(1);
  });

  it('should render out splitscreen stadiums if watching MLB opponent', () => {
    const props = merge({}, defaultTestProps, {
      watching: {
        opponentLineupId: 3,
      },
    });
    const wrapper = renderComponent(props);

    expect(wrapper.find(LiveMLBStadium)).to.have.length(2);
  });
});
