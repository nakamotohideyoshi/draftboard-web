import 'babel-core/polyfill';
import React from 'react'
const ReactRedux = require('react-redux')
const store = require('../../store')
const renderComponent = require('../../lib/render-component')
const CollectionMatchFilter = require('../filters/collection-match-filter.jsx')
const CollectionSearchFilter = require('../filters/collection-search-filter.jsx')
const PlayerListRow = require('./draft-player-list-row.jsx')
import DraftTeamFilter from './draft-team-filter.jsx'
import {forEach as _forEach, find as _find, matchesProperty as _matchesProperty} from 'lodash'
import * as moment from 'moment'
import {fetchDraftGroupIfNeeded, setFocusedPlayer, updateFilter, updateOrderByFilter}
  from '../../actions/draft-group-players-actions.js'
import {fetchDraftGroupBoxScoresIfNeeded, setActiveDraftGroupId}
  from '../../actions/upcoming-draft-groups-actions.js'
import {fetchSportInjuries} from '../../actions/injury-actions.js'
import {createLineupViaCopy, fetchUpcomingLineups, createLineupAddPlayer, removePlayer,
  editLineupInit, importLineup } from '../../actions/lineup-actions.js'
import {draftGroupPlayerSelector} from '../../selectors/draft-group-players-selector.js'
import {activeDraftGroupBoxScoresSelector} from '../../selectors/draft-group-info-selector.js'
// Other components that will take care of themselves on the draft page.
import './draft-player-detail.jsx'
// Router stuff
import { Router, Route } from 'react-router'
import {updatePath, syncReduxAndRouter} from 'redux-simple-router'
import createBrowserHistory from 'history/lib/createBrowserHistory'
const history = createBrowserHistory()
syncReduxAndRouter(history, store)



/**
 * Render a list of players able to be drafted.
 */
const DraftPlayerList = React.createClass({

  propTypes: {
    fetchDraftGroupBoxScoresIfNeeded: React.PropTypes.func.isRequired,
    fetchDraftGroupIfNeeded: React.PropTypes.func.isRequired,
    fetchUpcomingLineups: React.PropTypes.func.isRequired,
    filters: React.PropTypes.object.isRequired,
    createLineupViaCopy: React.PropTypes.func.isRequired,
    editLineupInit: React.PropTypes.func,
    importLineup: React.PropTypes.func,
    allPlayers: React.PropTypes.object,
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
    activeDraftGroupBoxScores: React.PropTypes.object
  },


  // Contest type filter data.
  playerPositionFilters: {
    'nba': [
      {title: 'All', column: 'position', match: ''},
      {title: 'PG', column: 'position', match: 'pg'},
      {title: 'SG', column: 'position', match: 'sg'},
      {title: 'SF', column: 'position', match: 'sf'},
      {title: 'PF', column: 'position', match: 'pf'},
      {title: 'C', column: 'position', match: 'c'}
    ],
    'nfl': [
      {title: 'All', column: 'position', match: ''},
      {title: 'QB', column: 'position', match: 'qb'},
      {title: 'RB', column: 'position', match: 'rb'},
      {title: 'WR', column: 'position', match: 'wr'},
      {title: 'TE', column: 'position', match: 'te'},
      {title: 'DST', column: 'position', match: 'dst'}
    ],
    'nhl': [
      {title: 'All', column: 'position', match: ''},
      {title: 'G', column: 'position', match: 'g'},
      {title: 'C', column: 'position', match: 'c'},
      {title: 'F', column: 'position', match: 'f'},
      {title: 'D', column: 'position', match: 'd'}
    ],
    'mlb': [
      {title: 'All', column: 'position', match: ''},
      {title: 'SP', column: 'position', match: 'sp'},
      {title: 'C', column: 'position', match: 'c'},
      {title: '1B', column: 'position', match: '1b'},
      {title: '2B', column: 'position', match: '2b'},
      {title: '3B', column: 'position', match: '3b'},
      {title: 'SS', column: 'position', match: 'ss'},
      {title: 'OF', column: 'position', match: 'of'}
    ]
  },


  loadData: function() {
    this.props.setActiveDraftGroupId(this.props.params.draftgroupId)
    this.props.fetchDraftGroupBoxScoresIfNeeded(this.props.params.draftgroupId)
    // Fetch draftgroup and lineups, once we have those we can do most anything in this section.
    Promise.all([
      this.props.fetchDraftGroupIfNeeded(this.props.params.draftgroupId),
      this.props.fetchUpcomingLineups(this.props.params.draftgroupId)
    ]).then( () => {
      // If the url has told us that the user wants to copy (import) a lineup, do that.
      if (this.props.params.lineupAction === 'copy' && this.props.params.lineupId) {
        this.props.createLineupViaCopy(this.props.params.lineupId)
      }
      // if we're editing...
      else if (this.props.params.lineupAction === 'edit' && this.props.params.lineupId) {
        let lineup = this.props.lineups[this.props.params.lineupId]
        this.props.importLineup(lineup, true)
        this.props.editLineupInit(this.props.params.lineupId)
      }
    })
  },


  getInitialState: function() {
    return ({
      showTeamFilter: false,
      filteredPlayers: [],
      newLineup: {
        availablePositions: []
      }
    });
  },


  getDefaultProps: function() {
    return {
      allPlayers: []
    };
  },


  //TODO: Make keyboard keys select players in the list.
  componentWillMount: function() {
    // Listen to j/k keypress actions to focus players.
    // KeypressActions.keypressJ.listen(this.focusNextRow);
    // KeypressActions.keypressK.listen(this.focusPreviousRow);
    this.loadData();
  },


  handleFilterChange: function(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match)
  },


  handleGameCountClick: function() {
    this.setState({showTeamFilter: true})
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
    let gameCount = ''
    if (this.props.draftGroupTime) {
      gameCount = Object.keys(this.props.activeDraftGroupBoxScores).length + ' Games'
    }

    let visibleRows = [];

    // Build up a list of rows to be displayed.
    _forEach(this.props.filteredPlayers, function(row) {
      let draftable = true
      let drafted = false
      // Is there a slot available?
      if (this.props.availablePositions.indexOf(row.position) === -1) {
        draftable = false
      }

      // Is the player already drafted?
      if (undefined !== _find(this.props.newLineup, _matchesProperty('player', row))) {
        draftable = false
        drafted = true
      }

      visibleRows.push(
        <PlayerListRow
          key={row.player_id}
          row={row}
          draftable={draftable}
          drafted={drafted}
          focusPlayer={this.props.focusPlayer}
          draftPlayer={this.props.draftPlayer}
          unDraftPlayer={this.props.unDraftPlayer}
        />
      )
    }.bind(this))



    // If the draftgroup hasn't been fetched yet, show a loading indicator.
    if(this.props.allPlayers === {}) {
      visibleRows = <tr><td colSpan="7"><h4>Loading Players.</h4></td></tr>
    }

    let positions = []
    if (this.props.sport && this.playerPositionFilters.hasOwnProperty(this.props.sport)) {
      positions = this.playerPositionFilters[this.props.sport]
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
            filterProperty='player.name'
            match=''
            onUpdate={this.handleFilterChange}
          />

          <CollectionMatchFilter
            className="collection-filter--player-type"
            filters={positions}
            filterName="positionFilter"
            filterProperty='position'
            match=''
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
                onClick={this.handleSetOrderBy.bind(null, 'name')}>Player</th>
              <th>Status</th>
              <th onClick={this.handleSetOrderBy.bind(null, 'team_alias')}>OPP</th>
              <th onClick={this.handleSetOrderBy.bind(null, 'fppg')}>AVG</th>
              <th>History</th>
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
  }

});


// Redux integration
let {Provider, connect} = ReactRedux;

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    allPlayers: state.draftGroupPlayers.allPlayers || {},
    filteredPlayers: draftGroupPlayerSelector(state),
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
    orderByProperty: state.draftGroupPlayers.filters.orderBy.property
  };
}

// Which action creators does it want to receive by props?
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
    setActiveDraftGroupId: (draftGroupId) => dispatch(setActiveDraftGroupId(draftGroupId))
  };
}

// Wrap the component to inject dispatch and selected state into it.
var DraftPlayerListConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(DraftPlayerList);

renderComponent(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/draft/:draftgroupId/" component={DraftPlayerListConnected} />
      <Route path="/draft/:draftgroupId/lineup/:lineupId/:lineupAction" component={DraftPlayerListConnected} />
    </Router>
  </Provider>,
  '.cmp-player-list'
);


module.exports = DraftPlayerList;
