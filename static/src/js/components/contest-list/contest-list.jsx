"use strict";

var React = require("react");
var Reflux = require('reflux');
var ContestStore = require("../../stores/contest-store.js");
var renderComponent = require('../../lib/render-component');
var DataTable = require('../data-table/data-table.jsx');
var DataTableColumnMatchFilter = require('../data-table/data-table-column-match-filter.jsx');
var Tr = require('./contest-list-tr.jsx');
var KeypressActions = require('../../actions/keypress-actions');
var AppActions = require('../../actions/app-actions');
var ContestActions = require('../../actions/contest-actions');
require('./contest-list-detail.jsx');


/**
 * Render a list (table) of contests.
 */
var ContestList = React.createClass({

  mixins: [
    Reflux.connect(ContestStore)
  ],


  getInitialState: function() {
    return ({
      // League filter data.
      leagueFilters: [
        {title: 'All', column: 'league', match: ''},
        {title: 'NBA', column: 'league', match: 'nba'},
        {title: 'NFL', column: 'league', match: 'nfl'},
        {title: 'MLB', column: 'league', match: 'mlb'}
      ],

      // Contest type filter data.
      contestTypeFilters: [
        {title: 'All', column: 'contestType', match: ''},
        {title: 'GPP', column: 'contestType', match: 'gpp'},
        {title: 'Head-to-Head', column: 'contestType', match: 'h2h'},
        {title: 'Double Up', column: 'contestType', match: 'double-up'}
      ],

      // Optional - Which columns in each data row should be displayed?
      columns: [
        'id',
        'title',
        'entries_total',
        'entries_filled',
        'prize',
        'startTime'
      ],

      // Optional - Map keys in the data row columns to a table header title.
      columnHeaders: {
        'title': 'Contest',
        'entries_total': 'Total Entries',
        'entries_filled': 'Entries Filled',
        'prize': 'Prize Pool',
        'startTime': 'Starting'
      }

    });
  },

  /**
   * When a row is clicked (or something else) we want to make that contest the 'focused' one.
   * @param {integer} id the ID of the contest to be focused.
   * @param {Object} e  Click event - Supplied by the click handler.
   */
  setContestFocus: function(id) {
    if (id !== 'undefined') {
      ContestActions.contestFocused(id);
      // Open the side pane.
      AppActions.openPane();
    }
  },

  componentWillMount: function() {
    // Listen to j/k keypress actions to focus contests.
    KeypressActions.keypressJ.listen(this.focusNextRow);
    KeypressActions.keypressK.listen(this.focusPreviousRow);
  },


  /**
   * Focus the next visible row in the contest list and open the detail pane.
   */
  focusNextRow: function() {
    this.setContestFocus(ContestStore.getNextVisibleRowId());
    // Open the side pane.
    AppActions.openPane();

  },


  /**
   * Focus the previous row in the contest list and open the detail pane.
   */
  focusPreviousRow: function() {
    this.setContestFocus(ContestStore.getPreviousVisibleRowId());
    // Open the side pane.
    AppActions.openPane();
  },


  render: function() {
    var contests = this.state.filteredContests || [];

    return (
      <div>
        <div className="clearfix">
          <DataTableColumnMatchFilter
            className="data-table-filter--league"
            filters={this.state.leagueFilters}
            column='league'
            match=''
          />

          <DataTableColumnMatchFilter
            className="data-table-filter--contest-type"
            filters={this.state.contestTypeFilters}
            column='contestType'
            match=''
          />
        </div>

        <DataTable
          data={contests}
          columns={this.state.columns}
          columnHeaders={this.state.columnHeaders}
          trComponent={Tr}
          sortKey={this.state.sortKey}
          sortDirection={this.state.sortDirection}
        />
      </div>
    );
  }

});


// Render the component.
renderComponent(<ContestList />, '.cmp-contest-list');


module.exports = ContestList;
