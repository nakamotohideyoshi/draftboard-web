import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
import LobbyContainer from '../../../components/lobby/lobby-container.jsx';
import allContestsFix from '../../../fixtures/json/redux-state/upcoming-contests/all-contests.js';
import UpcomingContestSelectorFix from '../../../fixtures/json/selectors-output/contest-pools-selector.js';
// This is an example of a data payload from a pusher contest_pool.upate event.
import pusherUpdateEventData from '../../../fixtures/json/pusher-event-data/contest-pool-update.js';

const defaultTestProps = {
  allContests: allContestsFix,
  draftGroupsWithLineups: [],
  contestFilters: {
    orderBy: {
      property: 'start',
      direction: 'asc',
    },
    sportFilter: {},
    skillLevelFilter: {
      filterProperty: 'skill_level',
      match: [
        'goodTestSkill',
      ],
    },
  },
  enterContest: () => true,
  featuredContests: [],
  fetchContestPoolEntries: () => true,
  fetchFeaturedContestsIfNeeded: () => true,
  fetchPrizeIfNeeded: () => true,
  fetchContestPools: () => true,
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
  removeContestPoolEntry: () => true,
  entrySkillLevels: {
    nba: 'bedTestSkill',
  },
  sportFilter: {
    match: 'nba',
    filterProperty: 'sport',
  },
  removeMessage: () => {
  },
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


  it('should render all of the contest pools.', () => {
    expect(wrapper.find('.cmp-contest-list__row')).to.have.length(
      Object.keys(defaultTestProps.filteredContests).length
    );
  });


  it('should render VETERAN LOBBY LOCKED modal.', () => {
    expect(wrapper.find('.cmp-skill-level-overlay.active')).to.have.length(1);
  });


  it('should not render VETERAN LOBBY LOCKED modal.', () => {
    wrapper.setProps({
      entrySkillLevels: {
        nba: 'goodTestSkill',
      },
    });
    expect(wrapper.find('.cmp-skill-level-overlay.active')).to.have.length(0);
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
