import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';
import merge from 'lodash/merge';

import { LiveStandingsPane } from '../../../components/live/live-standings-pane.jsx';
import LivePMRProgressBar from '../../../components/live/live-pmr-progress-bar.jsx';


/**
 * Tests for LiveMLBPitchZone
 */
describe('<LiveStandingsPane /> Component', () => {
  const renderComponent = (props) => mount(<LiveStandingsPane {...props} />);

  const defaultTestProps = {
    actions: {},
    lineups: {
      18: {
        draftGroupId: 17,
        id: 18,
        name: 'Example Lineup Name',
        roster: [
          331,
          101,
          381,
          205,
          9,
          92,
          103,
          25,
        ],
        sport: 'nba',
        fp: 51.75,
        timeRemaining: {
          duration: 384,
          decimal: 0.9999,
        },
        potentialWinnings: 18,
        rank: 1,
      },
      20: {
        draftGroupId: 17,
        id: 20,
        name: 'Example Lineup Name',
        roster: [
          406,
          25,
          269,
          389,
          261,
          103,
          381,
          357,
        ],
        sport: 'nba',
        fp: 21.75,
        timeRemaining: {
          duration: 384,
          decimal: 0.9999,
        },
        potentialWinnings: 0,
        rank: 2,
      },
    },
    hasLineupsUsernames: true,
    lineupsUsernames: {
      18: 'ppgogo',
      20: 'anson',
    },
    rankedLineups: [18, 20],
    watching: {
      contestId: 11,
      myLineupId: 18,
      myPlayerSRID: null,
      opponentLineupId: null,
      opponentPlayerSRID: null,
      sport: 'nba',
      draftGroupId: 17,
    },
    prizeStructure: {
      buyin: 1,
      payout_spots: 3,
      pk: 0,
      prize_pool: 0,
      ranks: [{
        category: 'cash',
        rank: 1,
        value: 1.8,
      }],
    },
  };

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render a div', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find('.live-standings-pane')).to.have.length(1);
  });

  it('should not render pitches if they do not exist', () => {
    const props = merge({}, defaultTestProps, {
      hasLineupsUsernames: false,
    });

    const wrapper = renderComponent(props);

    expect(wrapper.find('.live-standings-pane')).to.have.length('0');
  });

  it('should render standings properly', () => {
    const wrapper = renderComponent(defaultTestProps);

    expect(wrapper.find(LivePMRProgressBar)).to.have.length('2');
  });

  // TODO add in tests for iterativeRelaxation
});
