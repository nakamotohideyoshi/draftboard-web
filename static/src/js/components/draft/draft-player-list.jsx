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
import {fetchDraftGroupIfNeeded, setFocusedPlayer, updateFilter, fetchDraftGroupBoxScores
  } from '../../actions/draft-group-actions.js'
import {fetchSportInjuries} from '../../actions/injury-actions.js'
import {createLineupViaCopy, fetchUpcomingLineups, createLineupAddPlayer, removePlayer,
  editLineupInit, importLineup } from '../../actions/lineup-actions.js'
import {draftGroupPlayerSelector} from '../../selectors/draft-group-players-selector.js'
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
    fetchDraftGroupBoxScores: React.PropTypes.func.isRequired,
    fetchDraftGroupIfNeeded: React.PropTypes.func.isRequired,
    fetchUpcomingLineups: React.PropTypes.func.isRequired,
    filters: React.PropTypes.object.isRequired,
    createLineupViaCopy: React.PropTypes.func.isRequired,
    draftGroupBoxScores: React.PropTypes.array.isRequired,
    editLineupInit: React.PropTypes.func,
    importLineup: React.PropTypes.func,
    allPlayers: React.PropTypes.object,
    lineups: React.PropTypes.object,
    filteredPlayers: React.PropTypes.array,
    focusPlayer: React.PropTypes.func,
    draftPlayer: React.PropTypes.func,
    unDraftPlayer: React.PropTypes.func,
    newLineup: React.PropTypes.array,
    updateFilter: React.PropTypes.func,
    availablePositions: React.PropTypes.array,
    draftGroupTime: React.PropTypes.string,
    params: React.PropTypes.object
  },


  // Contest type filter data.
  playerPositionFilters: [
    {title: 'All', column: 'position', match: ''},
    {title: 'PG', column: 'position', match: 'pg'},
    {title: 'SG', column: 'position', match: 'sg'},
    {title: 'SF', column: 'position', match: 'sf'},
    {title: 'PF', column: 'position', match: 'pf'},
    {title: 'C', column: 'position', match: 'c'}
  ],


  loadData: function() {
    this.props.fetchDraftGroupBoxScores(this.props.params.draftgroupId)
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

  sortList: function(property) {
    console.log("sortList()", property);
    // DraftActions.setSortProperty(property);
  },


  handleFilterChange: function(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match)
  },


  render: function() {
    let formattedDraftTime = ''
    if (this.props.draftGroupTime) {
      formattedDraftTime = moment.utc(this.props.draftGroupTime).format('MMM Do YYYY, h:mma')
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

    return (
      <div>
        <h2 className="player-list__header">
          <span className="player-list__header-title">Draft a Team</span>
          <span className="player-list__header-divider">/</span>

          <span className="player-list__header-group">{formattedDraftTime}</span>
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
            filters={this.playerPositionFilters}
            filterName="positionFilter"
            filterProperty='position'
            match=''
            onUpdate={this.handleFilterChange}
          />
        </div>

        <div>
          <DraftTeamFilter
            games={this.props.draftGroupBoxScores}
            isVisible={false}
            onFilterChange={this.handleFilterChange}
            selectedTeams={this.props.filters.teamFilter.match}
            />
        </div>

        <table className="cmp-player-list__table table">
          <thead>
            <tr className="cmp-player-list__header-row">
              <th></th>
              <th>POS</th>
              <th></th>
              <th
                className="table__sortable"
                onClick={this.sortList.bind(this, 'name')}>Player</th>
              <th>Status</th>
              <th>OPP</th>
              <th>AVG</th>
              <th>History</th>
              <th
                className="table__sortable"
                onClick={this.sortList.bind(this, 'salary')}>Salary</th>
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
    allPlayers: state.draftDraftGroup.allPlayers || {},
    filteredPlayers: draftGroupPlayerSelector(state),
    filters: state.draftDraftGroup.filters,
    draftGroupTime: state.draftDraftGroup.start,
    draftGroupBoxScores: state.draftDraftGroup.boxScores,
    sport: state.draftDraftGroup.sport,
    lineups: state.upcomingLineups.lineups,
    newLineup: state.createLineup.lineup,
    availablePositions: state.createLineup.availablePositions,
    injuries: state.injuries,
    fantasyHistory: state.fantasyHistory
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    fetchDraftGroupBoxScores: (draftGroupId) => dispatch(fetchDraftGroupBoxScores(draftGroupId)),
    fetchDraftGroupIfNeeded: (draftGroupId) => dispatch(fetchDraftGroupIfNeeded(draftGroupId)),
    draftPlayer: (player) => dispatch(createLineupAddPlayer(player)),
    unDraftPlayer: (playerId) => dispatch(removePlayer(playerId)),
    focusPlayer: (playerId) => dispatch(setFocusedPlayer(playerId)),
    updateFilter: (filterName, filterProperty, match) => dispatch(updateFilter(filterName, filterProperty, match)),
    fetchUpcomingLineups: (draftGroupId) => dispatch(fetchUpcomingLineups(draftGroupId)),
    createLineupViaCopy: (lineupId) => dispatch(createLineupViaCopy(lineupId)),
    editLineupInit: (lineupId) => dispatch(editLineupInit(lineupId)),
    importLineup: (lineup, importTitle) => dispatch(importLineup(lineup, importTitle))
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
