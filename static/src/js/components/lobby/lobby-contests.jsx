import React from 'react'
const ReactRedux = require('react-redux')
const store = require('../../store')
const renderComponent = require('../../lib/render-component')
import {updateFilter} from '../../actions/upcoming-contests-actions.js'
var CollectionMatchFilter = require('../filters/collection-match-filter.jsx')
var CollectionSearchFilter = require('../filters/collection-search-filter.jsx')
var ContestRangeSliderFilter = require('../contest-list/contest-range-slider-filter.jsx')
var ContestList = require('../contest-list/contest-list.jsx')
import {upcomingContestSelector} from '../../selectors/upcoming-contest-selector.js'
import {fetchUpcomingContests, enterContest, setFocusedContest} from '../../actions/upcoming-contests-actions.js'
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
    focusedContestId: React.PropTypes.number,
    focusedLineupId: React.PropTypes.number,
    updateFilter: React.PropTypes.func,
    fetchUpcomingContests: React.PropTypes.func,
    fetchUpcomingDraftGroupsInfo: React.PropTypes.func,
    fetchEntries: React.PropTypes.func,
    enterContest: React.PropTypes.func,
    setFocusedContest: React.PropTypes.func
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
    this.props.fetchEntries()
  },


  // When one of the contest filters change.
  handleFilterChange: function(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match)
  },


  // Enter the currently focused lineup into a contest.
  handleEnterContest: function(contestId) {
    this.props.enterContest(contestId, this.props.focusedLineupId)
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
          focusedContestId={this.props.focusedContestId}
          setFocusedContest={this.props.setFocusedContest}
          enterContest={this.handleEnterContest}
        />
      </div>
    );
  }

});



// Redux integration
let {Provider, connect} = ReactRedux;

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    allContests: state.upcomingContests.allContests,
    focusedContestId: state.upcomingContests.allPlayers,
    focusedLineupId: state.upcomingLineups.focusedLineupId,
    filteredContests: upcomingContestSelector(state)
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
    setFocusedContest: (contestId) => dispatch(setFocusedContest(contestId))
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
