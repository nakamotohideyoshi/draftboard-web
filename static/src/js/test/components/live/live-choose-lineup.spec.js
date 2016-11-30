import nock from 'nock';
import React from 'react';
import sinon from 'sinon';
import merge from 'lodash/merge';
import { expect } from 'chai';
import { mount } from 'enzyme';

import { LiveChooseLineup } from '../../../components/live/live-choose-lineup.jsx';
import LiveLoading from '../../../components/live/live-loading.jsx';


describe('<LiveChooseLineup /> Component', () => {
  const renderComponent = (props) => mount(<LiveChooseLineup {...props} />);

  const lineupsSameSportProps = {
    lineupsLoaded: true,
    selectLineup: () => {},
    lineups: [
      {
        id: 1,
        draftGroup: 1,
        contests: [2],
        name: 'Curry\'s Chicken',
        start: '2015-10-15T23:00:00Z',
        sport: 'nba',
      }, {
        id: 2,
        contests: [2],
        name: 'Worriers worry',
        draftGroup: 2,
        start: '2015-10-15T23:00:00Z',
        sport: 'nba',
      }, {
        id: 3,
        contest: 3,
        name: 'Kickass your jackass',
        draftGroup: 3,
        start: '2015-10-15T23:00:00Z',
        sport: 'nba',
      },
    ],
  };

  const lineupsDifferentSportProps = {
    lineupsLoaded: true,
    selectLineup: () => {},
    lineups: [
      {
        id: 1,
        draftGroup: 1,
        contest: 2,
        name: 'Curry\'s Chicken',
        start: '2015-10-15T23:00:00Z',
        sport: 'nba',
      },
      {
        id: 2,
        contest: 2,
        name: 'Worriers worry',
        draftGroup: 2,
        start: '2015-10-15T23:00:00Z',
        sport: 'mlb',
      },
      {
        id: 3,
        contest: 3,
        name: 'Kickass your jackass',
        draftGroup: 3,
        start: '2015-10-15T23:00:00Z',
        sport: 'nfl',
      },
    ],
  };

  afterEach(() => {
    document.body.innerHTML = '';
    nock.cleanAll();
  });

  it('should render section', () => {
    const wrapper = renderComponent(lineupsSameSportProps);

    expect(wrapper.find('.live-choose-lineup')).to.have.length(1);
  });

  it('should show message if no lineups to choose from', () => {
    const props = {
      lineupsLoaded: true,
      lineups: [],
      selectLineup: () => {},
    };
    const wrapper = renderComponent(props);

    expect(wrapper.find('.live-choose-lineup__option')).to.have.length(0);
  });

  it('should show LiveLoading if lineups not loaded yet', () => {
    const props = {
      lineupsLoaded: false,
      lineups: [],
      selectLineup: () => {},
    };
    const wrapper = renderComponent(props);

    expect(wrapper.find(LiveLoading)).to.have.length(1);
  });

  it('should run actions.updateWatchingAndPath(lineup) when clicked.', () => {
    // Update the default props with a spy function.
    const props = merge(
      {}, lineupsSameSportProps, {
        selectLineup: sinon.spy(),
      }
    );

    const wrapper = renderComponent(props);
    wrapper.find('.live-choose-lineup__option').first().simulate('click', () => {
      // Expect it to be called only once.
      expect(props.selectLineup.callCount()).to.equal(1);
    });
  });

  it('title should be select lineup as we are directly on the lineup selection', () => {
    const wrapper = renderComponent(lineupsSameSportProps);

    expect(wrapper.find('.live-choose-lineup__title').text()).to.equal('Choose a lineup');
  });

  it('should provide you with 3 lineups to choose from (according to props given)', () => {
    const wrapper = renderComponent(lineupsSameSportProps);

    expect(wrapper.find('.live-choose-lineup__option')).to.have.length(3);
  });

  it('it should force you to choose a sport if there is more than one', () => {
    const wrapper = renderComponent(lineupsDifferentSportProps);

    expect(wrapper.find('.live-choose-lineup__title').text()).to.equal('Choose a sport');
  });

  it('should provide you with 3 sports to choose from (according to props given)', () => {
    const wrapper = renderComponent(lineupsDifferentSportProps);

    expect(wrapper.find('.live-choose-lineup__option')).to.have.length(3);
  });
});
