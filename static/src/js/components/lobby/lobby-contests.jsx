import React from 'react'
const ReactRedux = require('react-redux')
const store = require('../../store')
const renderComponent = require('../../lib/render-component')
import {updateFilter} from '../../actions/upcoming-contests-actions.js'
var CollectionMatchFilter = require('../filters/collection-match-filter.jsx')
var CollectionSearchFilter = require('../filters/collection-search-filter.jsx')
var ContestRangeSliderFilter = require('../contest-list/contest-range-slider-filter.jsx')
var ContestList = require('../contest-list/contest-list.jsx')
import {fetchPrizeIfNeeded} from '../../actions/prizes.js'
import {upcomingContestSelector} from '../../selectors/upcoming-contest-selector.js'
import {
  fetchUpcomingContests, enterContest, setFocusedContest, updateOrderByFilter
} from '../../actions/upcoming-contests-actions.js'
import {fetchUpcomingDraftGroupsInfo} from '../../actions/upcoming-draft-groups-info-actions.js'
import {fetchEntries} from '../../actions/entries.js'

// These components are needed in the lobby, but will take care of rendering themselves.
require('../contest-list/contest-list-header.jsx');
require('../contest-list/contest-list-detail.jsx');


/**
 * The contest list section of the lobby.
 */
var LobbyContests = React.createClass({

  propTypes: {
    allContests: React.PropTypes.object,
    filteredContests: React.PropTypes.array,
    focusedContest: React.PropTypes.object,
    focusedLineup: React.PropTypes.object,
    updateFilter: React.PropTypes.func,
    fetchUpcomingContests: React.PropTypes.func,
    fetchUpcomingDraftGroupsInfo: React.PropTypes.func,
    fetchEntries: React.PropTypes.func,
    enterContest: React.PropTypes.func,
    setFocusedContest: React.PropTypes.func,
    fetchPrizeIfNeeded: React.PropTypes.func,
    updateOrderByFilter: React.PropTypes.func,
    orderByProperty: React.PropTypes.string,
    orderByDirection: React.PropTypes.string,
    draftGroupsWithLineups: React.PropTypes.array
  },


  getInitialState: function() {
    return ({
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

    if (window.dfs.user.isAuthenticated === true) {
      this.props.fetchEntries()
    }
  },


  // When one of the contest filters change.
  handleFilterChange: function(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match)
  },


  // Enter the currently focused lineup into a contest.
  handleEnterContest: function(contestId, e) {
    e.stopPropagation()
    this.props.enterContest(contestId, this.props.focusedLineup.id)
  },


  handleFocusContest: function(contest) {
    this.props.fetchPrizeIfNeeded(contest.prize_structure)
    this.props.setFocusedContest(contest.id)
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
          focusedContest={this.props.focusedContest}
          focusedLineup={this.props.focusedLineup}
          setFocusedContest={this.handleFocusContest}
          enterContest={this.handleEnterContest}
          setOrderBy={this.handleSetOrderBy}
          draftGroupsWithLineups={this.props.draftGroupsWithLineups}
        />
      </div>
    );
  }

});



// Redux integration
let {Provider, connect} = ReactRedux;

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  // TODO: Put this in a selector - where derived data *should* be.
  // get focused contest
  let focusedContest = {id: null}
  if (state.upcomingContests.allContests.hasOwnProperty(state.upcomingContests.focusedContestId)) {
    focusedContest = state.upcomingContests.allContests[state.upcomingContests.focusedContestId]
  }

  // get focused lineup
  let focusedLineup = {id: null}
  if (state.upcomingLineups.lineups.hasOwnProperty(state.upcomingLineups.focusedLineupId)) {
    focusedLineup = state.upcomingLineups.lineups[state.upcomingLineups.focusedLineupId]
  }


  return {
    allContests: state.upcomingContests.allContests,
    focusedContest,
    focusedLineup,
    filteredContests: upcomingContestSelector(state),
    orderByProperty: state.upcomingContests.filters.orderBy.property,
    orderByDirection: state.upcomingContests.filters.orderBy.direction,
    draftGroupsWithLineups: state.upcomingLineups.draftGroupsWithLineups
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    // focusPlayer: (playerId) => dispatch(setFocusedPlayer(playerId)),
    updateFilter: (filterName, filterProperty, match) => dispatch(updateFilter(filterName, filterProperty, match)),
    fetchUpcomingContests: () => dispatch(fetchUpcomingContests()),
    fetchUpcomingDraftGroupsInfo: () => dispatch(fetchUpcomingDraftGroupsInfo()),
    fetchEntries: () => dispatch(fetchEntries()),
    enterContest: (contestId, lineupId) => dispatch(enterContest(contestId, lineupId)),
    setFocusedContest: (contestId) => dispatch(setFocusedContest(contestId)),
    fetchPrizeIfNeeded: (prizeStructureId) => dispatch(fetchPrizeIfNeeded(prizeStructureId)),
    updateOrderByFilter: (property, direction) => dispatch(updateOrderByFilter(property, direction))
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
