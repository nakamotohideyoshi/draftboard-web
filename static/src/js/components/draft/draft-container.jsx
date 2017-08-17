import React from 'react';
import shallowCompare from 'react-addons-shallow-compare';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import log from '../../lib/logging.js';
import lazyLoadImage from '../../lib/lazy-load-image.js';
import renderComponent from '../../lib/render-component';
import CollectionSearchFilter from '../filters/collection-search-filter.jsx';
import playerPositionFilterData from '../filters/player-position-filter-data';
import DraftPlayerListRow from './draft-player-list-row.jsx';
import DraftTeamFilter from './draft-team-filter.jsx';
import DraftTableHeader from './draft-table-header.jsx';
import ProbablePitchersFilter from './probable-pitchers-filter.jsx';
import PlayerPositionFilter from './player-position-filter.jsx';
import forEach from 'lodash/forEach';
import findIndex from 'lodash/findIndex';
import { verifyLocation } from '../../actions/user';
import { addMessage } from '../../actions/message-actions.js';
import { getInProgressLocalLineup } from '../../lib/lineup-drafts';
import { fetchDraftGroupIfNeeded, setFocusedPlayer, updateFilter, updateOrderByFilter } from
  '../../actions/draft-group-players-actions.js';
import { fetchDraftGroupBoxScoresIfNeeded, setActiveDraftGroupId } from
  '../../actions/upcoming-draft-groups-actions.js';
import { createLineupViaCopy, fetchUpcomingLineups, createLineupAddPlayer, removePlayer,
  editLineupInit, importLineup } from '../../actions/upcoming-lineup-actions.js';
import { draftGroupPlayerSelector, filteredPlayersSelector } from '../../selectors/draft-group-players-selector.js';
import { activeDraftGroupBoxScoresSelector } from '../../selectors/draft-group-info-selector.js';
// Other components that will take care of themselves on the draft page.
import './draft-player-detail.jsx';
// Router stuff
import { push as routerPush } from 'react-router-redux';
import { Router, Route, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import RestrictedLocationConfirmModal from '../account/restricted-location-confirm-modal';
import DraftScoringModal from './draft-scoring-modal';
import ScoringInfo from '../contest-list/scoring-info';

const nbaarena = require('../../../img/blocks/live-animation-stage/nba-court.png');
const nflarena = require('../../../img/blocks/live-animation-stage/nfl-field.png');
const nhlarena = require('../../../img/blocks/live-animation-stage/nhl-rink.png');

const arenamap = [
  { sport: 'nfl', asset: nflarena },
  { sport: 'nba', asset: nbaarena },
  { sport: 'nhlarena', asset: nhlarena },
];

const getArenaAsset = (sport) => {
  for (let i = 0; i < arenamap.length; i++) {
    if (arenamap[i].sport === sport) {
      return arenamap[i].asset;
    }
  }
};
/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps(state) {
  return {
    allPlayers: draftGroupPlayerSelector(state),
    filteredPlayers: filteredPlayersSelector(state),
    activeDraftGroupBoxScores: activeDraftGroupBoxScoresSelector(state),
    filters: state.draftGroupPlayersFilters.filters,
    draftGroupTime: state.draftGroupPlayers.start,
    draftGroupUpdates: state.draftGroupUpdates.sports,
    sport: state.draftGroupPlayers.sport,
    teams: state.sports,
    lineups: state.upcomingLineups.lineups,
    newLineup: state.createLineup.lineup,
    newLineupExtra: state.createLineup,
    availablePositions: state.createLineup.availablePositions,
    injuries: state.injuries,
    fantasyHistory: state.fantasyHistory,
    orderByDirection: state.draftGroupPlayersFilters.filters.orderBy.direction,
    orderByProperty: state.draftGroupPlayersFilters.filters.orderBy.property,
    userLocation: state.user.location,
  };
}

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
function mapDispatchToProps(dispatch) {
  return {
    fetchDraftGroupBoxScoresIfNeeded: (draftGroupId) => dispatch(fetchDraftGroupBoxScoresIfNeeded(draftGroupId)),
    fetchDraftGroupIfNeeded: (draftGroupId) => dispatch(fetchDraftGroupIfNeeded(draftGroupId)),
    draftPlayer: (player) => dispatch(createLineupAddPlayer(player)),
    unDraftPlayer: (playerId) => dispatch(removePlayer(playerId)),
    focusPlayer: (playerId) => dispatch(setFocusedPlayer(playerId)),
    updateFilter: (filterName, filterProperty, match) => dispatch(updateFilter(filterName, filterProperty, match)),
    fetchUpcomingLineups: (draftGroupId) => dispatch(fetchUpcomingLineups(draftGroupId)),
    createLineupViaCopy: (lineupId) => dispatch(createLineupViaCopy(lineupId)),
    editLineupInit: (lineupId) => dispatch(editLineupInit(lineupId)),
    importLineup: (lineup, importTitle) => dispatch(importLineup(lineup, importTitle)),
    updateOrderByFilter: (property, direction) => dispatch(updateOrderByFilter(property, direction)),
    routerPush: (path) => dispatch(routerPush(path)),
    setActiveDraftGroupId: (draftGroupId) => dispatch(setActiveDraftGroupId(draftGroupId)),
    verifyLocation: () => dispatch(verifyLocation()),
  };
}


/**
 * Render a list of players able to be drafted.
 */
const DraftContainer = React.createClass({

  propTypes: {
    activeDraftGroupBoxScores: React.PropTypes.object,
    allPlayers: React.PropTypes.array,
    availablePositions: React.PropTypes.array,
    createLineupViaCopy: React.PropTypes.func.isRequired,
    draftGroupTime: React.PropTypes.string,
    draftGroupUpdates: React.PropTypes.object,
    draftPlayer: React.PropTypes.func,
    editLineupInit: React.PropTypes.func,
    fetchDraftGroupBoxScoresIfNeeded: React.PropTypes.func.isRequired,
    fetchDraftGroupIfNeeded: React.PropTypes.func.isRequired,
    fetchUpcomingLineups: React.PropTypes.func.isRequired,
    filteredPlayers: React.PropTypes.array,
    filters: React.PropTypes.object.isRequired,
    focusPlayer: React.PropTypes.func,
    importLineup: React.PropTypes.func.isRequired,
    lineups: React.PropTypes.object,
    newLineup: React.PropTypes.array,
    newLineupExtra: React.PropTypes.object,
    orderByDirection: React.PropTypes.string,
    orderByProperty: React.PropTypes.string,
    params: React.PropTypes.object,
    setActiveDraftGroupId: React.PropTypes.func.isRequired,
    sport: React.PropTypes.string,
    teams: React.PropTypes.object.isRequired,
    unDraftPlayer: React.PropTypes.func,
    updateFilter: React.PropTypes.func.isRequired,
    updateOrderByFilter: React.PropTypes.func,
    verifyLocation: React.PropTypes.func.isRequired,
    userLocation: React.PropTypes.object.isRequired,
  },


  getDefaultProps() {
    return {
      allPlayers: [],
    };
  },


  getInitialState() {
    return ({
      filteredPlayers: [],
      newLineup: {
        availablePositions: [],
      },
      scoringModalState: false,
    });
  },


  componentWillMount() {
    // First check if the user's location is valid. they will be prompted with a modal showing
    // them what they can do.
    this.props.verifyLocation();
    // load in draft group players and injuries and boxscores and stuff.
    // After that, look for an unsaved local lineup to import.
    this.loadData().then(() => {
      // Don't load in-progress lineups if we are editing an existing lineup.
      if (this.props.params.lineupAction !== 'edit') {
        log.info('Looking for in-progress lineup in localstorage to resume.');
        const lineup = this.lineupInProgress(this.props.params.draftgroupId);
        if (lineup) {
          log.info('in-progress lineup found, attempting to import.');
          this.props.importLineup({ players: lineup });
        }
      }
      return true;
    });

    // Initialize the lazy image loader for all player images.
    this.lazyLoader = lazyLoadImage('.photo img');
  },


  shouldComponentUpdate(nextProps, nextState) {
    return shallowCompare(this, nextProps, nextState);
  },


  componentDidUpdate() {
    // If the component gets re-render, have the lazyLoader check if there are
    // any images now in-view that should be loaded.
    this.lazyLoader.reloadImages();
  },


  // A place to keep our lazy image loader.
  lazyLoader: null,


  loadData() {
    this.props.setActiveDraftGroupId(this.props.params.draftgroupId);
    this.props.fetchDraftGroupBoxScoresIfNeeded(this.props.params.draftgroupId);
    // this.props.fetchPlayerUpdatesIfNeeded(this.props.params.sport);

    // Fetch draftgroup and lineups, once we have those we can do most anything in this section.
    // Wrap this in a promise for testing purposes.
    return new Promise((resolve) => Promise.all(
      [
        this.props.fetchDraftGroupIfNeeded(this.props.params.draftgroupId),
        this.props.fetchUpcomingLineups(this.props.params.draftgroupId),
      ]).then(() => {
        // Once we know we have data, we can perform any actions specified by the URL parameters.
        this.performUrlAction();
        return resolve();
      })
    );
  },


  performUrlAction() {
    // If the url has told us that the user wants to copy (import) a lineup, do that.
    if (this.props.params.lineupAction === 'copy' && this.props.params.lineupId) {
      this.props.createLineupViaCopy(this.props.params.lineupId);
    } else if (this.props.params.lineupAction === 'edit' && this.props.params.lineupId) {
      // if we're editing...
      const lineup = this.props.lineups[this.props.params.lineupId];
      // Make sure we have the requested lineup.
      if (lineup) {
        this.props.importLineup(lineup, true);
        this.props.editLineupInit(this.props.params.lineupId);
      } else {
        store.dispatch(addMessage({
          header: 'Lineup Not Found',
          content: `We couldn't find the requested lineup. It's possible that the contest has started
          and you can no longer edit the lineup.`,
          level: 'warning',
        }));

        log.error(`lineup #${this.props.params.lineupId} not found.`);
      }
    }
  },


  lineupInProgress(draftGroupId) {
    return getInProgressLocalLineup(draftGroupId);
  },


  handleFilterChange(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match);
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


  renderLocationConfirmModalIfNeeded() {
    // If we know that they are in a blocked location because we have checked.
    if (
      this.props.userLocation.hasAttemptedToVerify &&
      !this.props.userLocation.isLocationVerified
    ) {
      // Show a modal warning them that they will not be able to do some things.
      return (
          <RestrictedLocationConfirmModal
            isOpen
            titleText="Location Unavailable"
            continueButtonText="Cool, got it"
            showCancelButton={false}
          >
            <div>{this.props.userLocation.message || 'Your location could not be verified.'}</div>
          </RestrictedLocationConfirmModal>
      );
    }
    // By default do not show confirm modal.
    return '';
  },

  render() {
    const self = this;
    const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${self.props.sport}`;

    let visibleRows = [];

    // Build up a list of rows to be displayed.
    forEach(self.props.allPlayers, (row) => {
      // determine if the player should be visible in the list.
      // We figure this out by seeing if the player is in the filteredPlayers list.
      const isVisible = findIndex(this.props.filteredPlayers, (player) =>
        player.player_id === row.player_id
      ) > -1;

      // Don't even bother rendering players that should not be seen.
      // I was hoping this would make swapping the visible/invisible states
      // faster, but it isn't.
      if (!isVisible) {
        return;
      }

      // Find the player's latest injury update, if one exists.
      let latestInjuryUpdate = {};

      if (
        this.props.sport in this.props.draftGroupUpdates
        && 'playerUpdates' in this.props.draftGroupUpdates[this.props.sport]
        && 'injury' in this.props.draftGroupUpdates[this.props.sport].playerUpdates
      ) {
        if (
          this.props.draftGroupUpdates[this.props.sport].playerUpdates.injury[row.player_srid]
          && this.props.draftGroupUpdates[this.props.sport].playerUpdates.injury[row.player_srid].length > 0
        ) {
          latestInjuryUpdate = this.props.draftGroupUpdates[this.props.sport].playerUpdates.injury[row.player_srid][0];
        }
      }

      visibleRows.push(
        <DraftPlayerListRow
          key={row.player_id}
          playerImagesBaseUrl={playerImagesBaseUrl}
          row={row}
          focusPlayer={self.props.focusPlayer}
          draftPlayer={self.props.draftPlayer}
          unDraftPlayer={self.props.unDraftPlayer}
          isVisible={isVisible}
          latestInjuryUpdate={latestInjuryUpdate}
        />
      );
    });


    // If the draftgroup hasn't been fetched yet, show a loading indicator.
    if (!this.props.allPlayers.length) {
      visibleRows = <tr><td colSpan="9"><h4>Loading Players.</h4></td></tr>;
    }

    let positions = [];

    if (this.props.sport && playerPositionFilterData.hasOwnProperty(this.props.sport)) {
      positions = playerPositionFilterData[this.props.sport];
    }

    return (
      <div>
        <header className="page-content__header">
          <h5 className="contest-list__sub_title">AVAILABLE PLAYERS</h5>
          <h2 className="player-list__header">
            <span className="player-list__header-title">Draft Your Team</span>
          </h2>

          <div className="player-list-filter-set">
            <CollectionSearchFilter
              className="collection-filter--player-name"
              filterName="playerSearchFilter"
              filterProperty="player.name"
              match=""
              onUpdate={this.handleFilterChange}
            />

            <ProbablePitchersFilter
              onUpdate={this.handleFilterChange}
              enabled={this.props.filters.probablePitchersFilter.match}
              sport={this.props.sport}
            />

            <PlayerPositionFilter
              positions={positions}
              handleFilterChange={this.handleFilterChange}
              newLineup={this.props.newLineup}
              activeFilter={this.props.filters.positionFilter}
            />

            <DraftScoringModal
              isOpen={this.state.scoringModalState}
              sport={this.props.sport}
              onClose={() => this.setState({
                scoringModalState: false,
              })}
            >
              <div>
                <div className="arena">
                  <img src={getArenaAsset(this.props.sport)} role="presentation" />
                </div>

                <ScoringInfo sport={this.props.sport} isModal />
              </div>
            </DraftScoringModal>

            <div
              className="button button--outline-alt1 export-button"
              onClick={() => this.setState({
                scoringModalState: !this.state.scoringModalState,
              })}
            >
              SCORING
            </div>
          </div>
        </header>
        <div>
          <DraftTeamFilter
            boxScores={this.props.activeDraftGroupBoxScores}
            onFilterChange={this.handleFilterChange}
            selectedTeams={this.props.filters.teamFilter.match}
            teams={this.props.teams}
            sport={this.props.sport}
          />
        </div>

        <table className="cmp-player-list__table table">
          <thead>
            <tr className="cmp-player-list__header-row">
              <th></th>
              <DraftTableHeader
                onClick={this.handleSetOrderBy}
                text="POS"
                sortParam="position"
              />
              <th></th>
              <DraftTableHeader
                onClick={this.handleSetOrderBy}
                text="Player"
                sortParam="name"
              />
              <DraftTableHeader
                onClick={this.handleSetOrderBy}
                text=""
                sortParam="status"
              />
              <DraftTableHeader
                onClick={this.handleSetOrderBy}
                text="GAME"
                sortParam="team_alias"
                additionalClasses=" padfix"
              />
              <DraftTableHeader
                onClick={this.handleSetOrderBy}
                text="AVG"
                sortParam="fppg"
                additionalClasses=" padfix"
              />
              <th className="padfix">Last 10</th>
              <DraftTableHeader
                onClick={this.handleSetOrderBy}
                text="Salary"
                sortParam="salary"
                additionalClasses=" padfix"
              />
            </tr>
          </thead>
          <tbody>{visibleRows}</tbody>
        </table>

        {this.renderLocationConfirmModalIfNeeded()}
      </div>
    );
  },

});


// Set up Redux connections to React
const { Provider, connect } = ReactRedux;

// Create an enhanced history that syncs navigation events with the store
const history = syncHistoryWithStore(browserHistory, store);

// Wrap the component to inject dispatch and selected state into it.
const DraftContainerConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(DraftContainer);

renderComponent(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/draft/:draftgroupId/" component={DraftContainerConnected} />
      <Route path="/draft/:draftgroupId/lineup/:lineupId/:lineupAction" component={DraftContainerConnected} />
    </Router>
  </Provider>,
  '.cmp-draft-container'
);


module.exports = DraftContainer;
