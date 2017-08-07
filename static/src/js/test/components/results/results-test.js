const utils = require('../../../lib/utils');
import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
import { Results } from '../../../components/results/results.jsx';


/**
 * Tests for Results
 */
describe('<Results /> Component', () => {
  const renderComponent = (props) => mount(<Results {...props} />);

  const defaultProps = {
    dispatch: () => ({}),
    hasRelatedInfo: true,
    params: {
      year: 2015,
      month: 1,
      day: 1,
    },
    route: {
      path: '',
    },
    routerPush: () => true,
    results: { isLoading: true },
    myCurrentLineupsSelector: {},
    liveContestsSelector: {},
    fetchUpcomingDraftGroupsInfo: () => true,
    fetchUpcomingLineups: () => true,
    fetchContestPoolEntries: () => true,
    fetchContestPools: () => true,
    fetchCurrentLineupsAndRelated: () => true,
    fetchResultsIfNeeded: () => true,
    upcominglineupsInfo: {},
    upcomingLineups: {},
    resultsWithLive: {
      lineups: [],
      overall: {
        winnings: 12,
        possible: 12,
        buyins: 12,
        entries: 12,
        contests: 12,
      },
    },
    sportsSelector: {},
  };

  let fakes = null;

  beforeEach(() => {
    fakes = sinon.collection;
  });

  afterEach(() => {
    fakes.restore();
    document.body.innerHTML = '';
  });

  it('should select yesterday if not date provided and it is before 10AM', () => {
    const wrapper = renderComponent(defaultProps);
    expect(wrapper.state().day).to.equal(1);
  });

  it('should select yesterday if not date provided and it is before 10AM', () => {
    const date = new Date(Date.UTC(2016, 3, 12, 12));  // second 12 refers to 12pm UTC
    fakes.stub(utils, 'dateNow', () => date);
    const wrapper = renderComponent(Object.assign(
      {},
      defaultProps,
      { params: {} }
    ));

    expect(wrapper.state().day).to.equal(11);
  });

  it('should select two days ago if not date provided and it is before 10AM', () => {
    const date = new Date(Date.UTC(2016, 3, 12, 9)).getTime();  // 9 refers to 9am UTC
    fakes.stub(utils, 'dateNow', () => date);
    const wrapper = renderComponent(Object.assign(
      {},
      defaultProps,
      { params: {} }
    ));

    expect(wrapper.state().day).to.equal(10);
  });
});
