'use strict';

var React = require('react');
var ReactRedux = require('react-redux');
var Reselect = require('reselect');
var store = require('../../store');
// var Reflux = require('reflux');
// var DraftGroupStore = require("../../stores/draft-group-store.js");
// var DraftNewLineupStore = require("../../stores/draft-new-lineup-store.js");
var renderComponent = require('../../lib/render-component');
var CollectionMatchFilter = require('../filters/collection-match-filter.jsx');
var CollectionSearchFilter = require('../filters/collection-search-filter.jsx');
var PlayerListRow = require('./draft-player-list-row.jsx');
var draftGroupActions = require('../../actions/draft-group-actions.js');
// var ContestActions = require('../../actions/contest-actions');
// var DraftActions = require("../../actions/draft-actions");
require('../contest-list/contest-list-header.jsx');
require('../contest-list/contest-list-detail.jsx');
require('../contest-list/contest-list-sport-filter.jsx');
require('./draft-player-detail.jsx');


/**
 * Render a list of players able to be drafted.
 */
var DraftPlayerList = React.createClass({

  // mixins: [
  //   Reflux.connect(DraftGroupStore),
  //   Reflux.connect(DraftNewLineupStore, 'newLineup')
  // ],


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
    draftGroupActions.fetchDraftGroup(draftgroupId);
  },


  getInitialState: function() {
    return ({
      filteredPlayers: [],
      newLineup: {
        availablePositions: []
      }
    });
  },


  /**
   * When a row is clicked (or something else) we want to make that contest the 'focused' one.
   * @param {integer} id the ID of the contest to be focused.
   */
  setContestFocus: function(id) {
    if (id !== 'undefined') {
      // ContestActions.contestFocused(id);
    }
  },


  //TODO: Make keyboard keys select players in the list.
  componentWillMount: function() {
    // Listen to j/k keypress actions to focus players.
    // KeypressActions.keypressJ.listen(this.focusNextRow);
    // KeypressActions.keypressK.listen(this.focusPreviousRow);
    this.loadData();
  },


  /**
   * Focus the next visible row in the contest list and open the detail pane.
   */
  focusNextRow: function() {
    // this.setContestFocus(ContestStore.getNextVisibleRowId());
  },


  /**
   * Focus the previous row in the contest list and open the detail pane.
   */
  focusPreviousRow: function() {
    // this.setContestFocus(ContestStore.getPreviousVisibleRowId());
  },


  sortList: function(property) {
    console.log("sortList()", property);
    // DraftActions.setSortProperty(property);
  },


  render: function() {
    // Build up a list of rows to be displayed.
    var visibleRows = this.state.filteredPlayers.map(function(row) {
      var draftable = true;
      // Is there a slot available?
      if (this.state.newLineup.availablePositions.indexOf(row.position) === -1) {
        draftable = false;
      }
      // Can we afford this player?
      if (this.state.newLineup.remainingSalary < row.salary) {
        draftable = false;
      }

      return (
        <PlayerListRow
          key={row.player_id}
          row={row}
          draftable={draftable}
        />
      );
    }, this);

    // If the draftgroup hasn't been fetched yet, show a loading indicator.
    if(!DraftGroupStore.allPlayers.length) {
      visibleRows = <tr><td colSpan="7"><h4>Loading Players.</h4></td></tr>;
    }

    return (
      <div>
        <div className="player-list-filter-set">
          <CollectionSearchFilter
            className="collection-filter--player-name"
            filterName="playerSearchFilter"
            filterProperty='player.name'
            match=''
            onUpdate={draftGroupActions.filterUpdated}
            onMount={draftGroupActions.registerFilter}
          />

        <CollectionMatchFilter
            className="collection-filter--player-type"
            filters={this.playerPositionFilters}
            filterName="contestTypeFilter"
            filterProperty='position'
            match=''
            onUpdate={draftGroupActions.filterUpdated}
            onMount={draftGroupActions.registerFilter}
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


// =============================================================================
// Redux integration

let {Provider, connect} = ReactRedux;
let {createSelector} = Reselect;

// Select portions of the state the component is interested in. Returned
// object will be merged with `this.props` of the connected component.
//
// Here the reselect library is used for creating memoized selectors.
//
let select = createSelector(
  // If all input selectors hit the cache, the pre-computed value for
  // the whole selector is returned and shouldComponentUpdate hook
  // (implemented by `react-redux`) will prevent component from
  // re-rendering.
  (state => state.contests),
  (contests) => {
    return { contests };
  }
);

// Wrap the component to inject dispatch and selected state into it.
var ContestNavConnected = connect(select)(ContestNav);

renderComponent(
  <Provider store={store}>
    <DraftPlayerList />
  </Provider>,
  '.cmp-player-list'
);



module.exports = DraftPlayerList;
