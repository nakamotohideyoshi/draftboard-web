import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
import LobbyContainer from '../../../components/lobby/lobby-container.jsx';
import ContestRangeSliderFilter from '../../../components/contest-list/contest-range-slider-filter.jsx';
import allContestsFix from '../../../fixtures/json/redux-state/upcoming-contests/all-contests.js';
import UpcomingContestSelectorFix from '../../../fixtures/json/selectors-output/upcoming-contest-selector.js';


const defaultTestProps = {
  allContests: allContestsFix,
  draftGroupsWithLineups: [],
  contestFilters: {
    orderBy: {
      property: 'start',
      direction: 'asc',
    },
    // Default to 'all' contest type matches.
    contestTypeFilter: {
      filterProperty: 'contestType',
      match: '',
    },
    contestFeeFilter: {
      match: { minVal: 0, maxVal: null },
    },
    contestSearchFilter: {},
    sportFilter: {},
  },
  enterContest: () => true,
  featuredContests: [],
  fetchContestPoolEntries: () => true,
  fetchFeaturedContestsIfNeeded: () => true,
  fetchPrizeIfNeeded: () => true,
  fetchUpcomingContests: () => true,
  fetchUpcomingDraftGroupsInfo: () => true,
  filteredContests: UpcomingContestSelectorFix,
  focusedContest: {},
  focusedLineup: {},
  hoveredLineupId: null,
  lineupsInfo: {},
  orderByDirection: 'asc',
  orderByProperty: 'start',
  setFocusedContest: () => true,
  updateFilter: () => true,
  updateOrderByFilter: () => true,
  routerPush: () => true,
  addMessage: () => true,
  upcomingContestUpdateReceived: () => true,
  // highestContestBuyin: React.PropTypes.number,
  removeContestPoolEntry: () => true,
};

// This is an example of a data payload from a pusher contest_pool.upate event.
const pusherUpdateEventData = {
  start: '2016-06-02T23:05:00Z',
  current_entries: 1,
  sport: 'mlb',
  prize_structure: {
    id: 20,
    name: '$100 10 Entry Tournament',
    buyin: 100,
    ranks: [
      {
        rank: 1,
        value: 400,
      },
      {
        rank: 2,
        value: 300,
      },
      {
        rank: 3,
        value: 200,
      },
    ],
    prize_pool: 900,
    is_h2h: false,
  },
  entries: 0,
  status: 'scheduled',
  max_entries: 3,
  buyin: 100,
  name: '$100 MLB 10-Man Tourney',
  id: 1522,
  contest_size: 10,
  draft_group: 1784,
  prize_pool: 900,
};


describe('<LobbyContainer /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<LobbyContainer {...props} />);
  }


  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  afterEach(() => {
    document.body.innerHTML = '';
  });


  it('should render contest filters.', () => {
    expect(wrapper.find('.contest-list-filter-set')).to.have.length(1);
    expect(wrapper.find('.contest-list-filter--contest-type')).to.have.length(1);
    expect(wrapper.find(ContestRangeSliderFilter)).to.have.length(1);
    expect(wrapper.find('.contest-list-filter--contest-name')).to.have.length(1);
  });


  it('should render all of the contest pools.', () => {
    expect(wrapper.find('.cmp-contest-list__row')).to.have.length(
      Object.keys(defaultTestProps.filteredContests).length
    );
  });


  it('should run upcomingContestUpdateReceived when onContestUpdateReceived is run', () => {
    // Add a spy.
    sinon.spy(defaultTestProps, 'upcomingContestUpdateReceived');
    // Re-mount the component with the spy.
    wrapper = renderComponent(defaultTestProps);
    const instance = wrapper.instance();
    // Run the thing that gets run when a pusher event comes through.
    instance.onContestUpdateReceived(pusherUpdateEventData);
    // Make sure that thing was run.
    expect(defaultTestProps.upcomingContestUpdateReceived.callCount).to.equal(1);
  });
});
