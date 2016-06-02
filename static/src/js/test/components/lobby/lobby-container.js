import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
import LobbyContainer from '../../../components/lobby/lobby-container.jsx';


const defaultTestProps = {
  allContests: {},
  draftGroupsWithLineups: [],
  enterContest: () => true,
  featuredContests: [],
  fetchContestPoolEntries: () => true,
  fetchFeaturedContestsIfNeeded: () => true,
  fetchPrizeIfNeeded: () => true,
  fetchUpcomingContests: () => true,
  fetchUpcomingDraftGroupsInfo: () => true,
  filteredContests: [],
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


  it('should render a filter set div.', () => {
    expect(wrapper.find('.contest-list-filter-set')).to.have.length(1);
  });


  it('should do stuff when onContestUpdateReceived is run', () => {
    // Add a spy.
    sinon.spy(defaultTestProps, 'upcomingContestUpdateReceived');
    // Re-mount the component with the spy.
    wrapper = renderComponent(defaultTestProps);
    const instance = wrapper.instance();
    // Run the thing that gets run when a pusher event comes through.
    instance.onContestUpdateReceived({
      eventData: 'eventDataHere',
    });
    // Make sure that thing was run.
    expect(defaultTestProps.upcomingContestUpdateReceived.callCount).to.equal(1);
  });
});
