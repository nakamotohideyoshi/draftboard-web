import React from 'react';
import * as ReactRedux from 'react-redux';
import Cookies from 'js-cookie';
import store from '../../store';
import log from '../../lib/logging';
import { push as routerPush } from 'react-router-redux';
import { fetchContestPoolEntries } from '../../actions/contest-pool-actions';
import { fetchFeaturedContestsIfNeeded } from '../../actions/featured-contest-actions';
import { fetchPrizeIfNeeded } from '../../actions/prizes';
import { lineupFocused } from '../../actions/upcoming-lineup-actions';
import { fetchUser } from '../../actions/user';
import { fetchContestPools, enterContest, setFocusedContest, updateOrderByFilter }
  from '../../actions/contest-pool-actions';
import { fetchUpcomingDraftGroupsInfo } from '../../actions/upcoming-draft-groups-actions';
import { focusedContestInfoSelector, focusedLineupSelector, entrySkillLevelsSelector }
  from '../../selectors/lobby-selectors';
import { contestPoolsSelector } from '../../selectors/contest-pools-selector';
import { upcomingLineupsInfo } from '../../selectors/upcoming-lineups-info';
import { upcomingContestUpdateReceived } from '../../actions/contest-pool-actions';
import * as AppActions from '../../stores/app-state-store';
import ContestList from '../contest-list/contest-list';
import SkillLevelOverlay from '../contest-list/skill-level-overlay';
import renderComponent from '../../lib/render-component';
import ContestListConfirmModal from '../contest-list/contest-list-confirm-modal';
import { addMessage, removeMessage } from '../../actions/message-actions';
import { removeParamFromURL } from '../../lib/utils';
import Pusher from '../../lib/pusher';

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
    allContests: state.contestPools.allContests,
    contestFilters: state.contestPools.filters,
    draftGroupsWithLineups: state.upcomingLineups.draftGroupsWithLineups,
    entrySkillLevels: entrySkillLevelsSelector(state),
    featuredContests: state.featuredContests.banners,
    filteredContests: contestPoolsSelector(state),
    focusedContest: focusedContestInfoSelector(state),
    focusedLineup: focusedLineupSelector(state),
    hoveredLineupId: state.upcomingLineups.hoveredLineupId,
    isFetchingContestPools: state.contestPools.isFetchingContestPools,
    lineupsInfo: upcomingLineupsInfo(state),
    orderByDirection: state.contestPools.filters.orderBy.direction,
    orderByProperty: state.contestPools.filters.orderBy.property,
    queryAction: state.routing.locationBeforeTransitions.query.action,
    hasFetchedLineups: state.upcomingLineups.hasFetchedLineups,
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
    fetchContestPoolEntries: () => dispatch(fetchContestPoolEntries()),
    fetchFeaturedContestsIfNeeded: () => dispatch(fetchFeaturedContestsIfNeeded()),
    fetchPrizeIfNeeded: (prizeStructureId) => dispatch(fetchPrizeIfNeeded(prizeStructureId)),
    fetchContestPools: () => dispatch(fetchContestPools()),
    fetchUpcomingDraftGroupsInfo: () => dispatch(fetchUpcomingDraftGroupsInfo()),
    fetchUser: () => dispatch(fetchUser()),
    lineupFocused: (lineupId) => dispatch(lineupFocused(lineupId)),
    setFocusedContest: (contestId) => dispatch(setFocusedContest(contestId)),
    updateOrderByFilter: (property, direction) => dispatch(
      updateOrderByFilter(property, direction)
    ),
    routerPush: (path) => dispatch(routerPush(path)),
    addMessage: (options) => dispatch(addMessage(options)),
    removeMessage: (options) => dispatch(removeMessage(options)),
    upcomingContestUpdateReceived: (contest) => dispatch(upcomingContestUpdateReceived(contest)),
  };
}


/**
 * The contest list section of the lobby.
 */
const LobbyContainer = React.createClass({

  propTypes: {
    addMessage: React.PropTypes.func,
    removeMessage: React.PropTypes.func,
    allContests: React.PropTypes.object,
    contestFilters: React.PropTypes.object,
    draftGroupsWithLineups: React.PropTypes.array,
    enterContest: React.PropTypes.func,
    entrySkillLevels: React.PropTypes.object.isRequired,
    featuredContests: React.PropTypes.array,
    fetchContestPoolEntries: React.PropTypes.func,
    fetchContestPools: React.PropTypes.func,
    fetchFeaturedContestsIfNeeded: React.PropTypes.func,
    fetchPrizeIfNeeded: React.PropTypes.func,
    fetchUpcomingDraftGroupsInfo: React.PropTypes.func,
    fetchUser: React.PropTypes.func.isRequired,
    filteredContests: React.PropTypes.array,
    focusedContest: React.PropTypes.object,
    focusedLineup: React.PropTypes.object,
    hasFetchedLineups: React.PropTypes.bool.isRequired,
    hoveredLineupId: React.PropTypes.number,
    isFetchingContestPools: React.PropTypes.bool.isRequired,
    lineupsInfo: React.PropTypes.object,
    lineupFocused: React.PropTypes.func,
    orderByDirection: React.PropTypes.string,
    orderByProperty: React.PropTypes.string,
    queryAction: React.PropTypes.string,
    removeContestPoolEntry: React.PropTypes.func,
    routerPush: React.PropTypes.func,
    setFocusedContest: React.PropTypes.func,
    upcomingContestUpdateReceived: React.PropTypes.func,
    updateOrderByFilter: React.PropTypes.func,
  },


  getInitialState() {
    return {
      showConfirmModal: false,
      contestToEnter: null,
    };
  },


  componentWillMount() {
    // Fetch all of the necessary data for the lobby.
    this.props.fetchContestPools();
    this.props.fetchUpcomingDraftGroupsInfo();

    log.info(`Action '${this.props.queryAction}' found in query params.`);
    // If the url indicates that a lineup was just saved, show a success message.
    if (this.props.queryAction === 'lineup-saved') {
      // remove the param from the URL.
      const strippedParams = removeParamFromURL(window.location.search, 'action');
      this.props.routerPush(`/contests/${strippedParams}`);
      this.props.addMessage({
        header: 'Lineup Saved! Now enter it into some contests',
        level: 'success',
        ttl: 5000,
      });
    }

    if (window.dfs.user.isAuthenticated === true) {
      this.props.fetchContestPoolEntries();
      this.props.fetchUser();
    }

    this.listenToSockets();
  },


  componentWillReceiveProps(nextProps) {
    // If we've fetched the user's lineups, and none exist, show a message.
    if (nextProps.hasFetchedLineups && Object.keys(nextProps.lineupsInfo).length === 0) {
      this.props.addMessage({
        header: 'Welcome to Draftboard. Create a lineup to get started.',
        level: 'success',
        id: 'create-lineup-message',
      });
    } else {
      this.props.removeMessage({ id: 'create-lineup-message' });
    }
  },


  onContestUpdateReceived(event) {
    // log.info('Pusher Event:', event);
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


    // used to separate developers into different channels, based on their django settings filename
    const channelPrefix = window.dfs.user.pusher_channel_prefix.toString();

    const contestChannel = Pusher.subscribe(`${channelPrefix}contest_pool`);
    contestChannel.bind('update', this.onContestUpdateReceived);
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
    this.props.routerPush(`/contests/${contest.id}/`);
    this.props.setFocusedContest(contest.id);
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
          entrySkillLevels={this.props.entrySkillLevels}
          isFetchingContestPools={this.props.isFetchingContestPools}
        />

        <ContestListConfirmModal
          confirmEntry={this.enterContest}
          cancelEntry={this.handleCancelEntry}
          contest={this.state.contestToEnter}
          lineup={this.props.focusedLineup}
          isOpen={this.state.showConfirmModal}
          lineupsInfo={this.props.lineupsInfo}
          entrySkillLevels = {this.props.entrySkillLevels}
        />

        <SkillLevelOverlay
          entrySkillLevels={this.props.entrySkillLevels}
          skillLevelFilter={this.props.contestFilters.skillLevelFilter}
          focusedLineup={this.props.focusedLineup}
        />
      </div>
    );
  },

});


// Wrap the component to inject dispatch and selected state into it.
const LobbyContainerConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(LobbyContainer);

renderComponent(
  <Provider store={store}>
    <LobbyContainerConnected />
  </Provider>,
  '.cmp-lobby-contests'
);

// Export the React component.
module.exports = LobbyContainer;
// Export the store-injected ReactRedux component.
export default LobbyContainerConnected;
