import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveHeader from '../../../components/live/live-header.jsx';
import LiveOverallStats from '../../../components/live/live-overall-stats.jsx';


describe('<LiveHeader /> Component', () => {
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
      opponentLineup: { isLoading: true },
      watching: {
        myLineupId: 2,
        contestId: null,
        opponentLineupId: null,
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find(LiveOverallStats)).to.have.length(0);
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
      opponentLineup: { isLoading: true },
      watching: {
        myLineupId: 2,
        contestId: null,
        opponentLineupId: null,
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find(LiveOverallStats)).to.have.length(1);
    expect(wrapper.find(LiveOverallStats).node.props.id).to.equal(2);
  });

  it('should only render contest rank and potentialWinnings if contest mode', () => {
    const props = {
      contest: {
        id: 3,
        isLoading: false,
        potentialWinnings: 25,  // relevant field
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
      opponentLineup: { isLoading: true },
      watching: {
        myLineupId: 2,
        contestId: 3,
        opponentLineupId: null,
      },
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find(LiveOverallStats)).to.have.length(1);
    expect(wrapper.find(LiveOverallStats).node.props.potentialWinnings).to.equal(25);
    expect(wrapper.find(LiveOverallStats).node.props.rank).to.equal(1);
  });

  it('should render mine and opponent stats when opponent chosen', () => {
    const props = {
      contest: {
        id: 3,
        isLoading: false,
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

    expect(wrapper.find(LiveOverallStats)).to.have.length(2);
    expect(wrapper.find(LiveOverallStats).at(0).node.props.id).to.equal(2);
    expect(wrapper.find(LiveOverallStats).at(1).node.props.id).to.equal(4);
    expect(wrapper.find('.live-overall-stats__vs')).to.have.length(1);

    // should still be using contest based winnings in vs mode
    expect(wrapper.find(LiveOverallStats).at(0).node.props.potentialWinnings).to.equal(25);
  });
});
