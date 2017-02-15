import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';
import proxyquire from 'proxyquire';


describe('<LiveHeader /> Component', () => {
  // use proxyquire to mock in responses
  const LiveHeader = proxyquire('../../../components/live/live-header', {
    './live-overall-stats': {
      LiveOverallStatsConnected: ({}) => (<div className="live-overall-stats"></div>),
    },
  }).default;

  const renderComponent = (props) => mount(<LiveHeader {...props} />);


  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should show nothing if still loading', () => {
    const props = {
      contest: { isLoading: true },  // relevant field
      myLineup: {
        isLoading: true,
      },
      lineups: [],
      selectLineup: () => {},
      opponentLineup: { isLoading: true },
      watching: {
        myLineupId: 2,
        contestId: null,
        opponentLineupId: null,
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('.live-overall-stats')).to.have.length(0);
  });

  it('should only render my lineup stats if no contest', () => {
    const props = {
      contest: { isLoading: true },  // relevant field
      myLineup: {
        fp: 32,
        id: 2,
        isLoading: false,
        name: 'My Name',
        potentialWinnings: 50,
        timeRemaining: {
          decimal: 0.5,
          duration: 88,
        },
      },
      lineups: [],
      selectLineup: () => {},
      opponentLineup: { isLoading: true },
      watching: {
        myLineupId: 2,
        contestId: null,
        opponentLineupId: null,
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('.live-overall-stats')).to.have.length(1);
  });

  it('should only render contest rank and potentialWinnings if contest mode', () => {
    const props = {
      contest: {
        id: 3,
        isLoading: false,
        potentialWinnings: 25,  // relevant field
        rank: 1,
      },
      lineups: [],
      selectLineup: () => {},
      myLineup: {
        isLoading: false,
        potentialWinnings: 80,
        fp: 32,
        id: 2,
        name: 'My Name',
        timeRemaining: {
          decimal: 0.5,
          duration: 88,
        },
      },
      opponentLineup: { isLoading: true },
      watching: {
        myLineupId: 2,
        contestId: 3,
        opponentLineupId: null,
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('.live-overall-stats')).to.have.length(1);
  });

  it('should render mine and opponent stats when opponent chosen', () => {
    const props = {
      contest: {
        id: 3,
        isLoading: false,
        name: 'Foo',
        potentialWinnings: 25,
        rank: 1,
      },
      myLineup: {
        isLoading: false,
        potentialWinnings: 80,
        fp: 32,
        id: 2,
        name: 'My Name',
        timeRemaining: {
          decimal: 0.5,
          duration: 88,
        },
      },
      lineups: [],
      selectLineup: () => {},
      opponentLineup: {
        isLoading: false,
        potentialWinnings: 20,
        fp: 23,
        id: 4,
        name: 'THE Opponent Lineup',
        timeRemaining: {
          decimal: 0.3,
          duration: 24,
        },
      },
      watching: {
        myLineupId: 2,
        contestId: 3,
        opponentLineupId: 4,
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('.live-overall-stats')).to.have.length(2);
    expect(wrapper.find('.live-header__contest-name')).to.have.length(1);
  });
});
