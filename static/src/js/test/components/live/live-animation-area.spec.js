import merge from 'lodash/merge';
import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveAnimationArea from '../../../components/live/live-animation-area.jsx';
import LiveMLBStadium from '../../../components/live/mlb/live-mlb-stadium.jsx';
import LiveNBACourt from '../../../components/live/nba/live-nba-court.jsx';


/**
 * Tests for LiveAnimationArea
 */
describe('<LiveAnimationArea /> Component', () => {
  const renderComponent = (props) => mount(<LiveAnimationArea {...props} />);

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

  it('should render out NBA court if watching NBA lineup', () => {
    const props = merge({}, defaultTestProps, {
      watching: {
        sport: 'nba',
      },
    });
    const wrapper = renderComponent(props);

    expect(wrapper.find(LiveNBACourt)).to.have.length('1');
  });
});
