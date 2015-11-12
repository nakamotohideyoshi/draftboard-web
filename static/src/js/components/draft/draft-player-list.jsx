import React from 'react'
const ReactRedux = require('react-redux')
const store = require('../../store')
const renderComponent = require('../../lib/render-component')
const CollectionMatchFilter = require('../filters/collection-match-filter.jsx')
const CollectionSearchFilter = require('../filters/collection-search-filter.jsx')
const PlayerListRow = require('./draft-player-list-row.jsx')
import { fetchDraftGroup, setFocusedPlayer, updateFilter } from '../../actions/draft-group-actions.js'
import { forEach as _forEach } from 'lodash'
import { draftGroupPlayerSelector } from '../../selectors/draft-group-players-selector.js'

// Other components that will take care of themselves on the draft page.
import './draft-player-detail.jsx'


/**
 * Render a list of players able to be drafted.
 */
const DraftPlayerList = React.createClass({

  propTypes: {
    fetchDraftGroup: React.PropTypes.func.isRequired,
    allPlayers: React.PropTypes.object,
    filteredPlayers: React.PropTypes.array,
    focusPlayer: React.PropTypes.func,
    newLineup: React.PropTypes.array,
    updateFilter: React.PropTypes.func
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
    // TODO: this sucks fix this.
    let draftgroupId = window.location.pathname.split('/')[2];

    this.props.fetchDraftGroup(draftgroupId);
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
    let visibleRows = [];

    // Build up a list of rows to be displayed.
    _forEach(this.props.filteredPlayers, function(row) {
      var draftable = true;
      // // Is there a slot available?
      // if (this.props.newLineup.availablePositions.indexOf(row.position) === -1) {
      //   draftable = false;
      // }
      // // Can we afford this player?
      // if (this.props.newLineup.remainingSalary < row.salary) {
      //   draftable = false;
      // }

      visibleRows.push(
        <PlayerListRow
          key={row.player_id}
          row={row}
          draftable={draftable}
          focusPlayer={this.props.focusPlayer}
        />
      );
    }.bind(this))



    // If the draftgroup hasn't been fetched yet, show a loading indicator.
    if(this.props.allPlayers === {}) {
      visibleRows = <tr><td colSpan="7"><h4>Loading Players.</h4></td></tr>
    }

    return (
      <div>
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

        <table className="cmp-player-list__table table">
          <thead>
            <tr className="cmp-player-list__header-row">
              <th>POS</th>
              <th></th>
              <th
                className="table__sortable"
                onClick={this.sortList.bind(this, 'name')}>Player</th>
              <th>Status</th>
              <th>OPP</th>
              <th>FPPG</th>
              <th
                className="table__sortable"
                onClick={this.sortList.bind(this, 'salary')}>Salary</th>
              <th></th>
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
    sport: state.draftDraftGroup.sport,
    newLineup: state.createLineup.lineup
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    fetchDraftGroup: (draftGroupId) => dispatch(fetchDraftGroup(draftGroupId)),
    focusPlayer: (playerId) => dispatch(setFocusedPlayer(playerId)),
    updateFilter: (filterName, filterProperty, match) => dispatch(updateFilter(filterName, filterProperty, match))
  };
}

// Wrap the component to inject dispatch and selected state into it.
var DraftPlayerListConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(DraftPlayerList);

renderComponent(
  <Provider store={store}>
    <DraftPlayerListConnected />
  </Provider>,
  '.cmp-player-list'
);


module.exports = DraftPlayerList;
