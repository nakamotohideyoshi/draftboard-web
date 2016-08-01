import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveUnsupported from '../../../components/live/live-unsupported.jsx';
import { Live } from '../../../components/live/live.jsx';


/**
 * Tests for Live
 */
describe('<Live /> Component', () => {
  const renderComponent = (props) => mount(<Live {...props} />);

  const defaultTestProps = {
    actions: {
      fetchCurrentLineupsAndRelated: () => ({}),
    },
    contest: { isLoading: true },
    draftGroupTiming: {},
    relevantGamesPlayers: {},
    myLineupInfo: { isLoading: true },
    opponentLineup: { isLoading: true },
    params: {},
    uniqueLineups: {},
    watching: {},
  };

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render message if under 768px', () => {
    const wrapper = renderComponent(defaultTestProps);

    wrapper.setState({ windowWidth: 700 });

    expect(wrapper.find(LiveUnsupported)).to.have.length(1);
  });
});
