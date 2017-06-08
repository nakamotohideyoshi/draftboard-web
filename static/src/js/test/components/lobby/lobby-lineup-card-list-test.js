import React from 'react';
import sinon from 'sinon';
// import merge from 'lodash/merge';
import { expect } from 'chai';
import { mount } from 'enzyme';
import LineupCardList from '../../../components/lobby/lobby-lineup-card-list.jsx';
import LineupCard from '../../../components/lineup/lineup-card.jsx';
// import LobbyDraftGroupSelectionModal from
//   '../../../components/lobby/lobby-draft-group-selection-modal.jsx';
import draftGroupInfoSelectorFix from '../../../fixtures/json/draft-group-info-selector.js';
import storeUpcomingLineupsFix from '../../../fixtures/json/store-upcoming-lineups.js';
import upcomingLineupsInfoSelectorFix from
  '../../../fixtures/json/upcoming-lineups-info-selector.js';
import upcomingLineupsBySportSelectorFix from
  '../../../fixtures/json/upcoming-lineups-by-sport-selector.js';

const defaultTestProps = {
  focusedSport: '',
  lineups: upcomingLineupsBySportSelectorFix,
  lineupsInfo: upcomingLineupsInfoSelectorFix,
  focusedLineupId: storeUpcomingLineupsFix.focusedLineupId,
  draftGroupInfo: draftGroupInfoSelectorFix,
  draftGroupSelectionModalIsOpen: false,
  openDraftGroupSelectionModal: () => true,
  // a promise that will always resolve.
  fetchUpcomingLineups: () => new Promise((resolve) => resolve()),
  removeContestPoolEntry: () => true,
};


describe('<LineupCardList /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<LineupCardList {...props} />);
  }

  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  // it('should render a <LobbyDraftGroupSelectionModal />', () => {
  //   expect(wrapper.find(LobbyDraftGroupSelectionModal)).to.have.length(1);
  // });


  it('should render a <LineupCard /> for each provided lineup.', () => {
    expect(wrapper.props('lineups').lineups.length).to.be.above(0);
    expect(wrapper.find(LineupCard)).to.have.length(wrapper.props('lineups').lineups.length);
  });


  it('should show a lineup creation CTA if no lineups are present.', () => {
    // should be showing a collapsed version since we have lineups by default.
    expect(wrapper.find('.cmp-lineup-card--create-collapsed')).to.have.length(0);
    expect(wrapper.find('.cmp-lineup-card--create')).to.have.length(0);
    wrapper.setProps({ lineups: [] });
    expect(wrapper.find('.cmp-lineup-card--create-collapsed')).to.have.length(0);
    expect(wrapper.find('.cmp-lineup-card--create')).to.have.length(1);
  });


  it('should fetch an authenticated users lineups on componentWillMount', () => {
    sinon.spy(defaultTestProps, 'fetchUpcomingLineups');
    window.dfs.user.isAuthenticated = true;

    // re-mount the component
    wrapper = renderComponent(defaultTestProps);
    expect(defaultTestProps.fetchUpcomingLineups.callCount).to.equal(1);
  });


  it('should NOT attemtp to fetch an unauthenticated users lineups on componentWillMount', () => {
    // Reset the previously set spy.
    defaultTestProps.fetchUpcomingLineups.reset();
    // 'log out' the user.
    window.dfs.user.isAuthenticated = false;

    // re-mount the component
    wrapper = renderComponent(defaultTestProps);
    expect(defaultTestProps.fetchUpcomingLineups.callCount).to.equal(0);
  });
});
