'use strict';

var React = require('react');
// var ContestStore = require('../../stores/contest-store.js');
var renderComponent = require('../../lib/render-component');
var ContestListRow = require('./contest-list-row.jsx');
var KeypressActions = require('../../actions/keypress-actions');
// var ContestActions = require('../../actions/contest-actions');
require('./contest-list-header.jsx');
require('./contest-list-detail.jsx');
require('./contest-list-sport-filter.jsx');


/**
 * Render a list (table) of contests.
 */
var ContestList = React.createClass({

  propTypes: {
    contests: React.PropTypes.array,
    focusedContestId: React.PropTypes.number
  },


  getDefaultProps: function() {
    return {
      contests: []
    };
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


  componentWillMount: function() {
    // Listen to j/k keypress actions to focus contests.
    KeypressActions.keypressJ.listen(this.focusNextRow);
    KeypressActions.keypressK.listen(this.focusPreviousRow);
  },


  /**
   * Focus the next visible row in the contest list.
   */
  focusNextRow: function() {
    // this.setContestFocus(ContestStore.getNextVisibleRowId());
  },


  /**
   * Focus the previous row in the contest list.
   */
  focusPreviousRow: function() {
    // this.setContestFocus(ContestStore.getPreviousVisibleRowId());
  },


  sortList: function(property) {
    // ContestActions.setSortProperty(property);
  },


  render: function() {
    var contests = this.props.contests || [];

    // Build up a list of rows to be displayed.
    var visibleRows = contests.map(function(row) {
      return (
        <ContestListRow
            key={row.id}
            row={row}
            focusedContestId={this.props.focusedContestId}
        />
      );
    }, this);


    return (
      <table className="cmp-contest-list__table table">
        <thead>
          <tr className="cmp-contest-list__header-row">
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'sport')}></th>
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'name')}>Contest</th>
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'entries')}>Entries / Size</th>
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'buyin')}>Fee</th>
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'prize_pool')}>Prizes</th>
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'start')}>Live In</th>
            <th></th>
          </tr>
        </thead>
        <tbody>{visibleRows}</tbody>
      </table>
    );
  }

});


// Render the component.
renderComponent(<ContestList />, '.cmp-contest-list');


module.exports = ContestList;
