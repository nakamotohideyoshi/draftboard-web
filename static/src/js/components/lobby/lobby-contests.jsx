import React from 'react';
import Pusher from 'pusher-js';
import * as ReactRedux from 'react-redux';
import Cookies from 'js-cookie';
import store from '../../store';
import { updatePath } from 'redux-simple-router';
import { fetchEntriesIfNeeded } from '../../actions/entries.js';
import { fetchFeaturedContestsIfNeeded } from '../../actions/featured-contest-actions.js';
import { fetchPrizeIfNeeded } from '../../actions/prizes.js';
import { fetchUpcomingContests, enterContest, setFocusedContest, updateOrderByFilter, }
  from '../../actions/upcoming-contests-actions.js';
import { fetchUpcomingDraftGroupsInfo } from '../../actions/upcoming-draft-groups-actions.js';
import { focusedContestInfoSelector, focusedLineupSelector, highestContestBuyin, }
  from '../../selectors/lobby-selectors.js';
import { upcomingContestSelector } from '../../selectors/upcoming-contest-selector.js';
import { upcomingLineupsInfo } from '../../selectors/upcoming-lineups-info.js';
import { updateFilter, upcomingContestUpdateReceived } from '../../actions/upcoming-contests-actions.js';
import * as AppActions from '../../stores/app-state-store.js';
import CollectionMatchFilter from '../filters/collection-match-filter.jsx';
import CollectionSearchFilter from '../filters/collection-search-filter.jsx';
import ContestList from '../contest-list/contest-list.jsx';
import ContestRangeSliderFilter from '../contest-list/contest-range-slider-filter.jsx';
import renderComponent from '../../lib/render-component';
import ContestListConfirmModal from '../contest-list/contest-list-confirm-modal.jsx';
import { addMessage } from '../../actions/message-actions.js';
import { removeParamFromURL } from '../../lib/utils.js';
// import log from '../../lib/logging.js';

// These components are needed in the lobby, but will take care of rendering themselves.
require('../contest-list/contest-list-header.jsx');
require('../contest-list/contest-list-detail.jsx');
const { Provider, connect } = ReactRedux;


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps(state) {
  return {
    allContests: state.upcomingContests.allContests,
    draftGroupsWithLineups: state.upcomingLineups.draftGroupsWithLineups,
    featuredContests: state.featuredContests.banners,
    filteredContests: upcomingContestSelector(state),
    focusedContest: focusedContestInfoSelector(state),
    focusedLineup: focusedLineupSelector(state),
    hoveredLineupId: state.upcomingLineups.hoveredLineupId,
    lineupsInfo: upcomingLineupsInfo(state),
    orderByDirection: state.upcomingContests.filters.orderBy.direction,
    orderByProperty: state.upcomingContests.filters.orderBy.property,
    highestContestBuyin: highestContestBuyin(state),
  };
}

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
function mapDispatchToProps(dispatch) {
  return {
    enterContest: (contestId, lineupId) => dispatch(enterContest(contestId, lineupId)),
    fetchEntriesIfNeeded: () => dispatch(fetchEntriesIfNeeded()),
    fetchFeaturedContestsIfNeeded: () => dispatch(fetchFeaturedContestsIfNeeded()),
    fetchPrizeIfNeeded: (prizeStructureId) => dispatch(fetchPrizeIfNeeded(prizeStructureId)),
    fetchUpcomingContests: () => dispatch(fetchUpcomingContests()),
    fetchUpcomingDraftGroupsInfo: () => dispatch(fetchUpcomingDraftGroupsInfo()),
    setFocusedContest: (contestId) => dispatch(setFocusedContest(contestId)),
    updateFilter: (filterName, filterProperty, match) => dispatch(updateFilter(filterName, filterProperty, match)),
    updateOrderByFilter: (property, direction) => dispatch(updateOrderByFilter(property, direction)),
    updatePath: (path) => dispatch(updatePath(path)),
    addMessage: (options) => dispatch(addMessage(options)),
    upcomingContestUpdateReceived: (contest) => dispatch(upcomingContestUpdateReceived(contest)),
  };
}


/**
 * The contest list section of the lobby.
 */
const LobbyContests = React.createClass({

  propTypes: {
    allContests: React.PropTypes.object,
    draftGroupsWithLineups: React.PropTypes.array,
    enterContest: React.PropTypes.func,
    featuredContests: React.PropTypes.array,
    fetchEntriesIfNeeded: React.PropTypes.func,
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
    updatePath: React.PropTypes.func,
    addMessage: React.PropTypes.func,
    upcomingContestUpdateReceived: React.PropTypes.func,
    highestContestBuyin: React.PropTypes.number,
  },


  getInitialState() {
    return {
      showConfirmModal: false,
      contestToEnter: null,
      contestTypeFilters: [
        { title: 'All', column: 'contestType', match: '' },
        { title: 'Guaranteed', column: 'contestType', match: 'gpp' },
        { title: 'Double-Up', column: 'contestType', match: 'double-up' },
        { title: 'Heads-Up', column: 'contestType', match: 'h2h' },
      ],
    };
  },


  componentWillMount() {
    // Fetch all of the necessary data for the lobby.
    this.props.fetchUpcomingContests();
    this.props.fetchUpcomingDraftGroupsInfo();
    this.props.fetchFeaturedContestsIfNeeded();

    // If the url indicates that a lineup was just saved, show a success message.
    if (window.location.search.indexOf('lineup-saved=true') !== -1) {
      // remove the param from the URL.
      const strippedParams = removeParamFromURL(window.location.search, 'lineup-saved');
      this.props.updatePath(`/lobby/${strippedParams}`);
      this.props.addMessage({
        header: 'Lineup Saved!',
        level: 'success',
        ttl: 5000,
      });
    }

    if (window.dfs.user.isAuthenticated === true) {
      this.props.fetchEntriesIfNeeded();
    }

    this.listenToSockets();
  },


  onContestUpdateReceived(event) {
    this.props.upcomingContestUpdateReceived(event);
  },


  listenToSockets() {
    // NOTE: this really bogs down your console, only use locally when needed
    // uncomment this ONLY if you need to debug why Pusher isn't connecting
    // Pusher.log = (message) => {
    //   if (window.console && window.console.log) {
    //     window.console.log(message);
    //   }
    // };

    const pusher = new Pusher(window.dfs.user.pusher_key, {
      encrypted: true,
    });

    // used to separate developers into different channels, based on their django settings filename
    const channelPrefix = window.dfs.user.pusher_channel_prefix.toString();

    const contestChannel = pusher.subscribe(`${channelPrefix}contest`);
    contestChannel.bind('update', this.onContestUpdateReceived);
  },


  // When one of the contest filters change.
  handleFilterChange(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match);
  },


  // Enter the currently focused lineup into a contest.
  handleEnterContest(contest) {
    // If the user has chosen not to confirm entries, enter the contest.
    if (Cookies.get('shouldConfirmEntry') === 'false') {
      this.enterContest(contest.id);
    } else {
          // Otherwise, show the confirmation modal.
      this.setState({
        showConfirmModal: true,
        contestToEnter: contest,
      });
    }
  },


  handleCancelEntry() {
    this.setState({
      showConfirmModal: false,
      contestToEnter: null,
    });
  },


  enterContest(contestId) {
    this.props.enterContest(contestId, this.props.focusedLineup.id);
  },


  handleFocusContest(contest) {
    this.props.updatePath(`/lobby/${contest.id}/`);
    this.props.setFocusedContest(contest.id);
    this.props.fetchPrizeIfNeeded(contest.prize_structure);
    AppActions.openPane();
  },


  handleSetOrderBy(propertyColumn) {
    // Determine sort direction based on current sort settings.
    let direction = 'desc';

    // If we are sorting by the already-'desc'-sorted column, flip the sort direction.
    if (propertyColumn === this.props.orderByProperty && this.props.orderByDirection === 'desc') {
      direction = 'asc';
    }
    // Dispatch the filter update.
    this.props.updateOrderByFilter(propertyColumn, direction);
  },


  render() {
    return (
      <div>
        <div className="contest-list-filter-set">
          <CollectionMatchFilter
            className="contest-list-filter--contest-type"
            filters={this.state.contestTypeFilters}
            filterName="contestTypeFilter"
            filterProperty="contestType"
            match=""
            onUpdate={this.handleFilterChange}
          />

          <div className="contest-list-filter-set__group">
            <ContestRangeSliderFilter
              className="contest-list-filter--contest-fee"
              filterName="contestFeeFilter"
              filterProperty="buyin"
              onUpdate={this.handleFilterChange}
              maxValLimit={this.props.highestContestBuyin}
            />

            <CollectionSearchFilter
              className="contest-list-filter--contest-name"
              filterName="contestSearchFilter"
              filterProperty="name"
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
          lineup={this.props.focusedLineup}
          isOpen={this.state.showConfirmModal}
          lineupsInfo={this.props.lineupsInfo}
        />
      </div>
    );
  },

});


// Wrap the component to inject dispatch and selected state into it.
const LobbyContestsConnected = connect(
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
