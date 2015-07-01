'use strict';

var React = require('react');


/**
 * Render a single DataTable table row.
 *
 * @param {Object} row - A single row of the DataTable's data.
 * @param {array} columns - The columns that should be displayed. This is directly passed down through DataTable.
 */
var TableDataTrMixin = {

  propTypes: {
    row: React.PropTypes.object.isRequired,
    columns: React.PropTypes.array
  },


  getInitialState: function() {
    return {limitColumns: false};
  },


  componentWillMount: function() {
    if (this.props.columns && this.props.columns.length > 0) {
      this.setState({limitColumns: true});
    }
  },


  /**
   * Determine if a td should be displayed based on the props.columns whitelist.
   *
   * @param  {string} column the key of the column
   * @return {boolean} should the td be displayed?
   */
  shouldDisplayColumn: function(column) {
    // If we're not limiting columns, show the column.
    if (!this.state.limitColumns) {
      return true;
    } else {
      // if we are limiting, and the column is not in the list, don't show it.
      if (this.props.columns.indexOf(column) === -1) {
        return false;
      }
      // If we're limiting, and the column is in the list, show it.
      return true;
    }
  }

};


module.exports = TableDataTrMixin;
