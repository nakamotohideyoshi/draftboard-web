import React from 'react'
const ReactRedux = require('react-redux')
const store = require('../../store')
const renderComponent = require('../../lib/render-component')
import {updateFilter} from '../../actions/upcoming-contests-actions.js'
var CollectionMatchFilter = require('../filters/collection-match-filter.jsx');
var CollectionSearchFilter = require('../filters/collection-search-filter.jsx');
var CollectionRangeSliderFilter = require('../filters/collection-range-slider-filter.jsx');
var ContestList = require('../contest-list/contest-list.jsx');
import { upcomingContestSelector } from '../../selectors/upcoming-contest-selector.js'
import {fetchUpcomingContests} from '../../actions/upcoming-contests-actions.js'
import {fetchUpcomingDraftGroupsInfo} from '../../actions/upcoming-draft-groups-info-actions.js'


// These components are needed in the lobby, but will take care of rendering themselves.
require('../contest-list/contest-list-header.jsx');
require('../contest-list/contest-list-detail.jsx');
// import '../contest-list/contest-list-detail.jsx'
// require('../contest-list/contest-list-sport-filter.jsx');


/**
 * The contest list section of the lobby.
 */
var LobbyContests = React.createClass({

  propTypes: {
    allContests: React.PropTypes.object,
    filteredContests: React.PropTypes.array,
    focusedContestId: React.PropTypes.number,
    updateFilter: React.PropTypes.func,
    fetchUpcomingContests: React.PropTypes.func,
    fetchUpcomingDraftGroupsInfo: React.PropTypes.func
  },


  getInitialState: function() {
    return ({
      // filteredContests: [],
      // Contest type filter data.
      contestTypeFilters: [
        {title: 'All', column: 'contestType', match: ''},
        {title: 'Guaranteed', column: 'contestType', match: 'gpp'},
        {title: 'Double-Up', column: 'contestType', match: 'double-up'},
        {title: 'Heads-Up', column: 'contestType', match: 'h2h'}
      ]
    });
  },


  componentWillMount: function() {
    this.props.fetchUpcomingContests()
    this.props.fetchUpcomingDraftGroupsInfo()
  },


  handleFilterChange: function(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match)
  },


  render: function() {




    // <CollectionRangeSliderFilter
    //   className="contest-list-filter--contest-fee"
    //   filterName="contestFeeFilter"
    //   filterProperty='fee'
    //   onUpdate={this.handleFilterChange}
    //  />

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
            //CollectionRangeSliderFilter
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
    filteredContests: upcomingContestSelector(state)
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    // focusPlayer: (playerId) => dispatch(setFocusedPlayer(playerId)),
    updateFilter: (filterName, filterProperty, match) => dispatch(updateFilter(filterName, filterProperty, match)),
    fetchUpcomingContests: () => dispatch(fetchUpcomingContests()),
    fetchUpcomingDraftGroupsInfo: () => dispatch(fetchUpcomingDraftGroupsInfo())
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
