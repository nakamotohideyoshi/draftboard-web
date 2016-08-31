import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import GameTime from '../../../components/site/game-time.jsx';


describe('<GameTime /> Component', () => {
  const renderComponent = (props) => mount(<GameTime {...props} />);

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render a div', () => {
    const props = {
      game: {
        sport: 'mlb',
        start: 1783403004,  // 2026-7-7 05:43
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('div.game-time')).to.have.length(1);
  });

  it('should render only start if game is scheduled', () => {
    const props = {
      game: {
        sport: 'mlb',
        start: 1783403004,  // 2026-7-7 05:43, FUTURE
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('.game-time--has-not-started')).to.have.length(1);
  });

  it('should render the word "Final" if game is complete', () => {
    const props = {
      game: {
        status: 'complete',
        start: 1436247804,  // 2015-7-7 05:43, PAST
        sport: 'mlb',
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('.game-time--game-complete').text()).to.equal('Final');
  });

  it('should default to unstarted if there is no inning or inning half', () => {
    const props = {
      game: {
        status: 'inprogress',
        start: 1436247804,  // 2015-7-7 05:43, PAST
        sport: 'mlb',
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('.game-time--has-not-started')).to.have.length(1);
  });

  it('should render innings if MLB game is in progress', () => {
    const props = {
      game: {
        boxscore: {
          inning: 7,
          inning_half: 'B',
        },
        status: 'inprogress',
        start: 1436247804,  // 2015-7-7 05:43, PAST
        sport: 'mlb',
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('.game-time--is-live')).to.have.length(1);
    expect(wrapper.find('.game-time__inning').text()).to.equal('7th');
    expect(wrapper.find('.game-time__half-inning--b')).to.have.length(1);
  });

  it('should default to unstarted if there is no clock or periodDisplay', () => {
    const props = {
      game: {
        status: 'inprogress',
        start: 1436247804,  // 2015-7-7 05:43, PAST
        sport: 'nba',
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('.game-time--has-not-started')).to.have.length(1);
  });

  it('should render innings if NBA game is in progress', () => {
    const props = {
      game: {
        boxscore: {
          clock: '5:43',
          periodDisplay: '4th',
        },
        status: 'inprogress',
        start: 1436247804,  // 2015-7-7 05:43, PAST
        sport: 'nba',
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('.game-time--is-live')).to.have.length(1);
    expect(wrapper.find('.game-time__clock').text()).to.equal('5:43');
    expect(wrapper.find('.game-time__period').text()).to.equal('4th');
  });
});
