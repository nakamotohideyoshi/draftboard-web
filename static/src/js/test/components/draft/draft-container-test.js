import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
import merge from 'lodash/merge';
import DraftContainer from '../../../components/draft/draft-container.jsx';
import CountdownClock from '../../../components/site/countdown-clock.jsx';
import CollectionSearchFilter from '../../../components/filters/collection-search-filter.jsx';
import CollectionMatchFilter from '../../../components/filters/collection-match-filter.jsx';
import DraftTeamFilter from '../../../components/draft/draft-team-filter.jsx';
import sportsStore from '../../../fixtures/json/store-sports.js';
import activeDraftGroupBoxScoresSelectorFix from '../../../fixtures/json/active-draft-group-box-scores-selector.js';


const defaultTestProps = {
  verifyLocation: () => true,
  fetchDraftGroupBoxScoresIfNeeded: () => true,
  fetchUpcomingDraftGroupUpdatesIfNeeded: () => true,
  fetchDraftGroupIfNeeded: () => Promise.resolve(),
  fetchUpcomingLineups: () => Promise.resolve(),
  importLineup: () => true,
  updateFilter: () => true,
  editLineupInit: () => true,
  filters: {
    orderBy: {
      property: 'salary',
      direction: 'desc',
    },
    playerSearchFilter: {
      filterProperty: 'player.name',
      match: '',
    },
    probablePitchersFilter: {
      // match == true means to only show probably pitchers.
      match: true,
      // this doesn't matter.
      filterProperty: 'srid',
    },
    positionFilter: {},
    teamFilter: {
      match: [],
      count: 0,
    },
  },
  userLocation: {
    status: 'unknown',
    isLocationVerified: false,
    isSending: false,
    hasAttemptedToVerify: false,
    message: null,
  },
  createLineupViaCopy: () => true,
  setActiveDraftGroupId: () => true,
  teams: sportsStore,
  activeDraftGroupBoxScores: activeDraftGroupBoxScoresSelectorFix,
  // URL Parameters from the URL router.
  params: {

  },
};


describe('<DraftContainer /> Component', () => {
  let wrapper;


  function renderComponent(props) {
    return mount(<DraftContainer {...props} />);
  }


  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render a header, filters, and table', () => {
    expect(wrapper.find('.player-list__header')).to.have.length(1);
    expect(wrapper.find('.player-list-filter-set')).to.have.length(1);
    expect(wrapper.find('.cmp-player-list__table')).to.have.length(1);
    expect(wrapper.find(DraftTeamFilter)).to.have.length(1);
    expect(wrapper.find(CollectionMatchFilter)).to.have.length(1);
    expect(wrapper.find(CollectionSearchFilter)).to.have.length(1);
  });

  it('should load data once mounted.', () => {
    const props = merge(
      {}, defaultTestProps, {
        setActiveDraftGroupId: sinon.spy(),
        fetchDraftGroupBoxScoresIfNeeded: sinon.spy(),
      }
    );

    wrapper = renderComponent(props);
    expect(props.fetchDraftGroupBoxScoresIfNeeded.callCount).to.equal(1);
    expect(props.setActiveDraftGroupId.callCount).to.equal(1);
  });


  it('should create a lineup copy if specifided in the params.', (done) => {
    const props = merge(
      {}, defaultTestProps, {
        createLineupViaCopy: sinon.spy(),
        params: {
          lineupAction: 'copy',
          lineupId: 666,
        },
      }
    );

    wrapper = renderComponent(props);

    wrapper.node.loadData().then(() => {
      // it should have been called once already by the component, but we
      // manually called it so we can tell when loadData was done. Because
      // of this it's callCount should be 2.
      expect(wrapper.node.props.createLineupViaCopy.callCount).to.equal(2);
      done();
    })
    .catch((err) => {
      done(err);
    });
  });


  it('should import and edit a lineup if specifided in the params.', (done) => {
    const props = merge(
      {}, defaultTestProps, {
        editLineupInit: sinon.spy(),
        importLineup: sinon.spy(),
        params: {
          lineupAction: 'edit',
          lineupId: 666,
        },
        lineups: {
          666: {},
        },
      }
    );

    wrapper = renderComponent(props);

    wrapper.node.loadData().then(() => {
      // it should have been called once already by the component, but we
      // manually called it so we can tell when loadData was done. Because
      // of this it's callCount should be 2.  -- add one more because of saved
      // draft imports.
      expect(wrapper.node.props.editLineupInit.callCount).to.equal(2);
      expect(wrapper.node.props.importLineup.callCount).to.equal(2);
      done();
    })
    .catch((err) => {
      done(err);
    });
  });
});
