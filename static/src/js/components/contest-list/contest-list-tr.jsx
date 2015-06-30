'use strict';

var React = require('react');
var Td = require('../data-table/data-table-td.jsx');
var AppActions = require('../../actions/app-actions');
var ContestActions = require('../../actions/contest-actions');
var ContestStore = require('../../stores/contest-store');
var DataTableTrMixin = require('../data-table/data-table-tr-mixin.jsx');


/**
 * Render a single ContestList table row. - This extends the base Tr with some
 * contest list specific functionality.
 *
 * Clicking the row sets it as the active contest in the Store.
 *
 * @param {Object} row - A single row of the DataTable's data.
 * @param {array} columns - The columns that should be displayed. This is directly passed down
 * through DataTable.
 */
var ContestListTr = React.createClass({
  mixins: [DataTableTrMixin],

  propTypes: {
    row: React.PropTypes.object.isRequired,
    columns: React.PropTypes.array
  },


  /**
   * When a row is clicked (or something else) we want to make that contest the 'focused' one.
   * @param {integer} id the ID of the contest to be focused.
   * @param {Object} e  Click event - Supplied by the click handler.
   */
  setContestFocus: function(id) {
    if (typeof id === 'number') {
      ContestActions.contestFocused(id);
      // Open the side pane.
      AppActions.openPane();
    }
  },


  render: function() {
    var cells = [];

    // If it's the currently focused contest, add a class to it.
    var classes = ContestStore.getFocusedContest() === this.props.row.id ? 'active' : '';


    // Loop through the row's propeties and create TD's from them.
    for (var prop in this.props.row) {
      if(this.shouldDisplayColumn(prop)) {
        if (this.props.row.hasOwnProperty(prop)) {
          cells.push(<Td
            key={this.props.row[prop]}
            cellName={prop}
            cellData={this.props.row[prop]}
          />);
        }
      }
    }

    return (
      <tr
        className={classes}
        onClick={this.setContestFocus.bind(this, this.props.row.id)}
        key={this.props.row.id}
      >
        {cells}
      </tr>
    );
  }

});


module.exports = ContestListTr;
