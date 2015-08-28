"use strict";

var React = require('react');
var Reflux = require('reflux');
var ContestStore = require("../../stores/contest-store.js");
var renderComponent = require('../../lib/render-component');
var ContestStorePropertyMatchFilter = require('./contest-store-property-match-filter.jsx');
var ContestListSearchFilter = require('./contest-list-search-filter.jsx');
var ContestListRow = require('./contest-list-row.jsx');
var ContestListDetail = require('./contest-list-detail.jsx');
var KeypressActions = require('../../actions/keypress-actions');
var ContestActions = require('../../actions/contest-actions');
require('./contest-list-header.jsx');
require('./contest-list-detail.jsx');
require('./contest-list-sport-filter.jsx');


/**
 * Render a list (table) of contests.
 */
var ContestList = React.createClass({

  mixins: [
    Reflux.connect(ContestStore)
  ],


  getInitialState: function() {
    return ({
      filteredContests: [],
      // Contest type filter data.
      contestTypeFilters: [
        {title: 'All', column: 'contestType', match: ''},
        {title: 'Guaranteed', column: 'contestType', match: 'gpp'},
        {title: 'Double-Up', column: 'contestType', match: 'double-up'},
        {title: 'Heads-Up', column: 'contestType', match: 'h2h'}
      ]
    });
  },


  /**
   * When a row is clicked (or something else) we want to make that contest the 'focused' one.
   * @param {integer} id the ID of the contest to be focused.
   */
  setContestFocus: function(id) {
    if (id !== 'undefined') {
      ContestActions.contestFocused(id);
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
  },


  /**
   * Focus the previous row in the contest list and open the detail pane.
   */
  focusPreviousRow: function() {
    this.setContestFocus(ContestStore.getPreviousVisibleRowId());
  },


  render: function() {
    var contests = this.state.filteredContests || [];
    // Build up a list of rows to be displayed.
    var visibleRows = contests.map(function(row) {
      // Determine if this row should have it's details shown as a TR after it.
      var detailRow;
      if (this.state.focusedContestId === row.id) {
        detailRow = <ContestListDetail key={row.id + '-detail'} />;
      }

      return (
        [<ContestListRow
          key={row.id}
          row={row}
          focusedContestId={this.state.focusedContestId} />,
        detailRow]
      );
    }, this);


    return (
      <div>
        <div className="contest-list-filter-set">
          <ContestStorePropertyMatchFilter
            className="contest-list-filter--contest-type"
            filters={this.state.contestTypeFilters}
            filterName="contestTypeFilter"
            property='contestType'
            match=''
          />

          <ContestListSearchFilter
            className="contest-list-filter--contest-type"
            filterName="contestSearchFilter"
            property='name'
            match=''
          />
        </div>

        <table className="cmp-contest-list__table table">
          <thead>
            <tr className="cmp-contest-list__header-row">
              <th></th>
              <th>Contest</th>
              <th>Entries / Size</th>
              <th>Fee</th>
              <th>Prizes</th>
              <th>Live In</th>
              <th></th>
            </tr>
          </thead>
          <tbody>{visibleRows}</tbody>
        </table>
      </div>
    );
  }

});


// Render the component.
renderComponent(<ContestList />, '.cmp-contest-list');


module.exports = ContestList;
