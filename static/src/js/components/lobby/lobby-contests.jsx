import React from 'react'
import * as ReactRedux from 'react-redux'
import Cookies from 'js-cookie'
import store from '../../store'
import {updatePath} from 'redux-simple-router'

import {fetchEntries} from '../../actions/entries.js'
import {fetchFeaturedContestsIfNeeded} from '../../actions/featured-contest-actions.js'
import {fetchPrizeIfNeeded} from '../../actions/prizes.js'
import {fetchUpcomingContests, enterContest, setFocusedContest, updateOrderByFilter}
  from '../../actions/upcoming-contests-actions.js'
import {fetchUpcomingDraftGroupsInfo} from '../../actions/upcoming-draft-groups-info-actions.js'
import {focusedContestInfoSelector} from '../../selectors/lobby-selectors.js'
import {upcomingContestSelector} from '../../selectors/upcoming-contest-selector.js'
import {upcomingLineupsInfo} from '../../selectors/upcoming-lineups-info.js'
import {updateFilter} from '../../actions/upcoming-contests-actions.js'
import * as AppActions from '../../stores/app-state-store.js'
import CollectionMatchFilter from '../filters/collection-match-filter.jsx'
import CollectionSearchFilter from '../filters/collection-search-filter.jsx'
import ContestList from '../contest-list/contest-list.jsx'
import ContestRangeSliderFilter from '../contest-list/contest-range-slider-filter.jsx'
import renderComponent from '../../lib/render-component'
import ContestListConfirmModal from '../contest-list/contest-list-confirm-modal.jsx'

// These components are needed in the lobby, but will take care of rendering themselves.
require('../contest-list/contest-list-header.jsx');
require('../contest-list/contest-list-detail.jsx');


/**
 * The contest list section of the lobby.
 */
var LobbyContests = React.createClass({

  propTypes: {
    allContests: React.PropTypes.object,
    draftGroupsWithLineups: React.PropTypes.array,
    enterContest: React.PropTypes.func,
    featuredContests: React.PropTypes.array,
    fetchEntries: React.PropTypes.func,
    fetchFeaturedContestsIfNeeded: React.PropTypes.func,
    fetchPrizeIfNeeded: React.PropTypes.func,
    fetchUpcomingContests: React.PropTypes.func,
    fetchUpcomingDraftGroupsInfo: React.PropTypes.func,
    filteredContests: React.PropTypes.array,
    focusedContest: React.PropTypes.object,
    focusedLineup: React.PropTypes.object,
    hoveredLineupId: React.PropTypes.number,
    lineupsInfo: React.PropTypes.object,
    orderByDirection: React.PropTypes.string,
    orderByProperty: React.PropTypes.string,
    setFocusedContest: React.PropTypes.func,
    updateFilter: React.PropTypes.func,
    updateOrderByFilter: React.PropTypes.func,
    updatePath: React.PropTypes.func
  },


  getInitialState: function() {
    return ({
      showConfirmModal: false,
      contestToEnter: null,
      contestTypeFilters: [
        {title: 'All', column: 'contestType', match: ''},
        {title: 'Guaranteed', column: 'contestType', match: 'gpp'},
        {title: 'Double-Up', column: 'contestType', match: 'double-up'},
        {title: 'Heads-Up', column: 'contestType', match: 'h2h'}
      ]
    });
  },


  componentWillMount: function() {
    // Fetch all of the necessary data for the lobby.
    this.props.fetchUpcomingContests()
    this.props.fetchUpcomingDraftGroupsInfo()
    this.props.fetchFeaturedContestsIfNeeded()

    if (window.dfs.user.isAuthenticated === true) {
      this.props.fetchEntries()
    }
  },


  // When one of the contest filters change.
  handleFilterChange: function(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match)
  },


  // Enter the currently focused lineup into a contest.
  handleEnterContest: function(contest, e) {
    e.stopPropagation()
    // If the user has chosen not to confirm entries, enter the contest.
    console.log(Cookies.get('shouldConfirmEntry'))
    if (Cookies.get('shouldConfirmEntry') === 'false') {
      this.enterContest(contest.id)
    }
    // Otherwise, show the confirmation modal.
    else {
      this.setState({
        showConfirmModal: true,
        contestToEnter: contest
      })
    }
  },


  handleCancelEntry: function() {
    this.setState({
      showConfirmModal: false,
      contestToEnter: null
    })
  },

  enterContest: function(contestId) {
    this.props.enterContest(contestId, this.props.focusedLineup.id)
  },


  handleFocusContest: function(contest) {
    this.props.updatePath(`/lobby/${contest.id}/`)
    this.props.setFocusedContest(contest.id)
    this.props.fetchPrizeIfNeeded(contest.prize_structure)
    AppActions.openPane();
  },


  handleSetOrderBy: function(propertyColumn) {
    // Determine sort direction based on current sort settings.
    let direction = 'desc'

    // If we are sorting by the already-'desc'-sorted column, flip the sort direction.
    if (propertyColumn === this.props.orderByProperty  && 'desc' === this.props.orderByDirection) {
      direction = 'asc'
    }
    // Dispatch the filter update.
    this.props.updateOrderByFilter(propertyColumn, direction)
  },


  render: function() {
    return (
      <div>
        <div className="contest-list-filter-set">
          <CollectionMatchFilter
            className="contest-list-filter--contest-type"
            filters={this.state.contestTypeFilters}
            filterName="contestTypeFilter"
            filterProperty='contestType'
            match=''
            onUpdate={this.handleFilterChange}
          />

          <div className="contest-list-filter-set__group">
            <ContestRangeSliderFilter
              className="contest-list-filter--contest-fee"
              filterName="contestFeeFilter"
              filterProperty='buyin'
              onUpdate={this.handleFilterChange}
             />

            <CollectionSearchFilter
              className="contest-list-filter--contest-name"
              filterName="contestSearchFilter"
              filterProperty='name'
              onUpdate={this.handleFilterChange}
            />
          </div>
        </div>

        <ContestList
          contests={this.props.filteredContests}
          draftGroupsWithLineups={this.props.draftGroupsWithLineups}
          enterContest={this.handleEnterContest}
          featuredContests={this.props.featuredContests}
          focusedContest={this.props.focusedContest}
          focusedLineup={this.props.focusedLineup}
          hoveredLineupId={this.props.hoveredLineupId}
          lineupsInfo={this.props.lineupsInfo}
          setFocusedContest={this.handleFocusContest}
          setOrderBy={this.handleSetOrderBy}
        />

      <ContestListConfirmModal
        confirmEntry={this.enterContest}
        cancelEntry={this.handleCancelEntry}
        contest={this.state.contestToEnter}
        isOpen={this.state.showConfirmModal}
      />
      </div>
    );
  }

});



// Redux integration
let {Provider, connect} = ReactRedux;

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  // get focused lineup
  let focusedLineup = {id: null}
  if (state.upcomingLineups.lineups.hasOwnProperty(state.upcomingLineups.focusedLineupId)) {
    focusedLineup = state.upcomingLineups.lineups[state.upcomingLineups.focusedLineupId]
  }


  return {
    allContests: state.upcomingContests.allContests,
    draftGroupsWithLineups: state.upcomingLineups.draftGroupsWithLineups,
    featuredContests: state.featuredContests.banners,
    filteredContests: upcomingContestSelector(state),
    focusedContest: focusedContestInfoSelector(state),
    focusedLineup,
    hoveredLineupId: state.upcomingLineups.hoveredLineupId,
    lineupsInfo: upcomingLineupsInfo(state),
    orderByDirection: state.upcomingContests.filters.orderBy.direction,
    orderByProperty: state.upcomingContests.filters.orderBy.property
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    enterContest: (contestId, lineupId) => dispatch(enterContest(contestId, lineupId)),
    fetchEntries: () => dispatch(fetchEntries()),
    fetchFeaturedContestsIfNeeded: () => dispatch(fetchFeaturedContestsIfNeeded()),
    fetchPrizeIfNeeded: (prizeStructureId) => dispatch(fetchPrizeIfNeeded(prizeStructureId)),
    fetchUpcomingContests: () => dispatch(fetchUpcomingContests()),
    fetchUpcomingDraftGroupsInfo: () => dispatch(fetchUpcomingDraftGroupsInfo()),
    setFocusedContest: (contestId) => dispatch(setFocusedContest(contestId)),
    updateFilter: (filterName, filterProperty, match) => dispatch(updateFilter(filterName, filterProperty, match)),
    updateOrderByFilter: (property, direction) => dispatch(updateOrderByFilter(property, direction)),
    updatePath: (path) => dispatch(updatePath(path))
  };
}

// Wrap the component to inject dispatch and selected state into it.
var LobbyContestsConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(LobbyContests);

renderComponent(
  <Provider store={store}>
    <LobbyContestsConnected />
  </Provider>,
  '.cmp-lobby-contests'
);


module.exports = LobbyContestsConnected;
