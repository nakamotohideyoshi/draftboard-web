import 'babel-core/polyfill';
import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import log from '../../lib/logging.js';
import renderComponent from '../../lib/render-component';
import CollectionMatchFilter from '../filters/collection-match-filter.jsx';
import CollectionSearchFilter from '../filters/collection-search-filter.jsx';
import DraftPlayerListRow from './draft-player-list-row.jsx';
import DraftTeamFilter from './draft-team-filter.jsx';
import { forEach as _forEach, filter as _filter } from 'lodash';
import { findIndex as _findIndex } from 'lodash';
import { fetchDraftGroupIfNeeded, setFocusedPlayer, updateFilter, updateOrderByFilter, }
  from '../../actions/draft-group-players-actions.js';
import { fetchDraftGroupBoxScoresIfNeeded, setActiveDraftGroupId, }
  from '../../actions/upcoming-draft-groups-actions.js';
import { createLineupViaCopy, fetchUpcomingLineups, createLineupAddPlayer, removePlayer,
  editLineupInit, importLineup } from '../../actions/lineup-actions.js';
import { draftGroupPlayerSelector, filteredPlayersSelector } from '../../selectors/draft-group-players-selector.js';
import { activeDraftGroupBoxScoresSelector } from '../../selectors/draft-group-info-selector.js';
// Other components that will take care of themselves on the draft page.
import './draft-player-detail.jsx';
// Router stuff
import { Router, Route } from 'react-router';
import { updatePath, syncReduxAndRouter } from 'redux-simple-router';
import createBrowserHistory from 'history/lib/createBrowserHistory';

const history = createBrowserHistory();
syncReduxAndRouter(history, store);
const { Provider, connect } = ReactRedux;


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
    filters: state.draftGroupPlayers.filters,
    draftGroupTime: state.draftGroupPlayers.start,
    sport: state.draftGroupPlayers.sport,
    teams: state.sports,
    lineups: state.upcomingLineups.lineups,
    newLineup: state.createLineup.lineup,
    newLineupExtra: state.createLineup,
    availablePositions: state.createLineup.availablePositions,
    injuries: state.injuries,
    fantasyHistory: state.fantasyHistory,
    orderByDirection: state.draftGroupPlayers.filters.orderBy.direction,
    orderByProperty: state.draftGroupPlayers.filters.orderBy.property,
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
    updatePath: (path) => dispatch(updatePath(path)),
    setActiveDraftGroupId: (draftGroupId) => dispatch(setActiveDraftGroupId(draftGroupId)),
  };
}


/**
 * Render a list of players able to be drafted.
 */
const DraftContainer = React.createClass({

  propTypes: {
    fetchDraftGroupBoxScoresIfNeeded: React.PropTypes.func.isRequired,
    fetchDraftGroupIfNeeded: React.PropTypes.func.isRequired,
    fetchUpcomingLineups: React.PropTypes.func.isRequired,
    filters: React.PropTypes.object.isRequired,
    createLineupViaCopy: React.PropTypes.func.isRequired,
    editLineupInit: React.PropTypes.func,
    importLineup: React.PropTypes.func,
    allPlayers: React.PropTypes.array,
    lineups: React.PropTypes.object,
    filteredPlayers: React.PropTypes.array,
    focusPlayer: React.PropTypes.func,
    draftPlayer: React.PropTypes.func,
    unDraftPlayer: React.PropTypes.func,
    newLineup: React.PropTypes.array,
    newLineupExtra: React.PropTypes.object,
    updateFilter: React.PropTypes.func,
    sport: React.PropTypes.string,
    availablePositions: React.PropTypes.array,
    draftGroupTime: React.PropTypes.string,
    teams: React.PropTypes.object.isRequired,
    params: React.PropTypes.object,
    orderByDirection: React.PropTypes.string,
    orderByProperty: React.PropTypes.string,
    updateOrderByFilter: React.PropTypes.func,
    setActiveDraftGroupId: React.PropTypes.func.isRequired,
    activeDraftGroupBoxScores: React.PropTypes.object,
  },


  getDefaultProps() {
    return {
      allPlayers: [],
    };
  },


  getInitialState() {
    return ({
      showTeamFilter: false,
      filteredPlayers: [],
      newLineup: {
        availablePositions: [],
      },
    });
  },


  // TODO: Make keyboard keys select players in the list.
  componentWillMount() {
    // Listen to j/k keypress actions to focus players.
    // KeypressActions.keypressJ.listen(this.focusNextRow);
    // KeypressActions.keypressK.listen(this.focusPreviousRow);
    this.loadData();
  },


  // Contest type filter data.
  playerPositionFilters: {
    nba: [
      { title: 'All', column: 'position', match: '' },
      { title: 'G', column: 'position', match: ['pg', 'sg'] },
      { title: 'F', column: 'position', match: ['sf', 'pf'] },
      { title: 'C', column: 'position', match: 'c' },
    ],
    nfl: [
      { title: 'All', column: 'position', match: '' },
      { title: 'QB', column: 'position', match: 'qb' },
      { title: 'RB', column: 'position', match: 'rb' },
      { title: 'WR', column: 'position', match: 'wr' },
      { title: 'TE', column: 'position', match: 'te' },
      { title: 'DST', column: 'position', match: 'dst' },
    ],
    nhl: [
      { title: 'All', column: 'position', match: '' },
      { title: 'G', column: 'position', match: 'g' },
      { title: 'C', column: 'position', match: 'c' },
      { title: 'F', column: 'position', match: 'f' },
      { title: 'D', column: 'position', match: 'd' },
    ],
    mlb: [
      { title: 'All', column: 'position', match: '' },
      { title: 'SP', column: 'position', match: 'sp' },
      { title: 'C', column: 'position', match: 'c' },
      { title: '1B', column: 'position', match: '1b' },
      { title: '2B', column: 'position', match: '2b' },
      { title: '3B', column: 'position', match: '3b' },
      { title: 'SS', column: 'position', match: 'ss' },
      { title: 'OF', column: 'position', match: 'of' },
    ],
  },


  loadData() {
    this.props.setActiveDraftGroupId(this.props.params.draftgroupId);
    this.props.fetchDraftGroupBoxScoresIfNeeded(this.props.params.draftgroupId);
    // Fetch draftgroup and lineups, once we have those we can do most anything in this section.
    Promise.all([
      this.props.fetchDraftGroupIfNeeded(this.props.params.draftgroupId),
      this.props.fetchUpcomingLineups(this.props.params.draftgroupId),
    ]).then(() => {
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
          log.error(`lineup #${this.props.params.lineupId} not found.`);
        }
      }
    }).catch((reason) => {
      log.error(reason);
    });
  },


  handleFilterChange(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match);
  },


  handleGameCountClick() {
    this.setState({ showTeamFilter: !this.state.showTeamFilter });
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


  // Determine whether a supplied player is in the lineup.
  isPlayerInLineup(lineup, player) {
    // Return a list of all matching players.
    const matchingPlayers = _filter(lineup, (slot) => {
      if (slot.player) {
        if (slot.player.player_id === player.player_id) {
          return true;
        }
      }
      return false;
    });

    // If the list of matching players is empty, the player is not in the lineup.
    return Object.keys(matchingPlayers).length > 0;
  },


  render() {
    const self = this;
    const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${self.props.sport}`;
    let gameCount = '';
    if (this.props.draftGroupTime) {
      gameCount = `${Object.keys(this.props.activeDraftGroupBoxScores).length} Games`;
    }

    let visibleRows = [];

    // Build up a list of rows to be displayed.
    _forEach(self.props.allPlayers, (row) => {
      // determine if the player should be visible in the list.
      // We figure this out by seeing if the player is in the filteredPlayers list.
      const isVisible = _findIndex(this.props.filteredPlayers, (player) =>
        player.player_id === row.player_id
      ) > -1;

      visibleRows.push(
        <DraftPlayerListRow
          key={row.player_id}
          playerImagesBaseUrl={playerImagesBaseUrl}
          row={row}
          focusPlayer={self.props.focusPlayer}
          draftPlayer={self.props.draftPlayer}
          unDraftPlayer={self.props.unDraftPlayer}
          isVisible={isVisible}
        />
      );
    });


    // If the draftgroup hasn't been fetched yet, show a loading indicator.
    if (this.props.allPlayers === {}) {
      visibleRows = <tr><td colSpan="7"><h4>Loading Players.</h4></td></tr>;
    }

    let positions = [];
    if (this.props.sport && this.playerPositionFilters.hasOwnProperty(this.props.sport)) {
      positions = this.playerPositionFilters[this.props.sport];
    }

    return (
      <div>
        <h2 className="player-list__header">
          <span className="player-list__header-title">Draft a Team</span>
          <span className="player-list__header-divider">/</span>
          <span
            className="player-list__header-games"
            onClick={this.handleGameCountClick}
          >{gameCount}</span>
        </h2>

        <div className="player-list-filter-set">
          <CollectionSearchFilter
            className="collection-filter--player-name"
            filterName="playerSearchFilter"
            filterProperty="player.name"
            match=""
            onUpdate={this.handleFilterChange}
          />

          <CollectionMatchFilter
            className="collection-filter--player-type"
            filters={positions}
            filterName="positionFilter"
            filterProperty="position"
            match=""
            onUpdate={this.handleFilterChange}
          />
        </div>

        <div>
          <DraftTeamFilter
            boxScores={this.props.activeDraftGroupBoxScores}
            isVisible={this.state.showTeamFilter}
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
              <th onClick={this.handleSetOrderBy.bind(null, 'position')}>POS</th>
              <th></th>
              <th
                className="table__sortable"
                onClick={this.handleSetOrderBy.bind(null, 'name')}
              >
                Player
              </th>
              <th>Status</th>
              <th onClick={this.handleSetOrderBy.bind(null, 'team_alias')}>OPP</th>
              <th onClick={this.handleSetOrderBy.bind(null, 'fppg')}>AVG</th>
              <th>Last 10</th>
              <th
                onClick={this.handleSetOrderBy.bind(null, 'salary')}
                className="table__sortable"
              >Salary</th>
            </tr>
          </thead>
          <tbody>{visibleRows}</tbody>
        </table>
      </div>
    );
  },

});


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
