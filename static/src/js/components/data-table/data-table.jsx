'use strict';

var React = require('react');
var Tr = require('./data-table-tr.jsx');
var ContestActions = require('../../actions/contest-actions');


/**
 * DataTable - Feed an array of data objects to this comonent and it will render into a <table>.
 *
 * @param {array|Object} data - An object containing rows of data to be displayed.
 * @param {array} columns - A list of columns that should be displayed - these need to match
 *        up with keys in the {data} object.
 * @param {Object} columnHeaders - The <th> headers will be auto-inferred by default. To override
 *        this, provide a map from {data} object keys to a string.
 */
var DataTable = React.createClass({

  propTypes: {
    data: React.PropTypes.oneOfType([React.PropTypes.object, React.PropTypes.array]).isRequired,
    // Pretty names for column header td's.
    // If these arent' supplied they will be inferred from the data's keys.
    columnHeaders: React.PropTypes.object,
    // A list of row keys that should be displayed in the table.
    columns: React.PropTypes.array,
    // Override the standard <tr> component.
    trComponent: React.PropTypes.any,
    sortKey: React.PropTypes.string,
    sortDirection: React.PropTypes.string
  },


  getInitialState: function() {
    return {};
  },


  getDefaultProps: function() {
    return {
      focusedContestId: null,
      data: []
    };
  },


  componentDidMount: function() {
    // Override the standard <tr> component if another is supplied.
    if (this.props.trComponent) {
      Tr = this.props.trComponent;
    }
  },


  /**
   * Determine if a column header (<th>) should be displayed.
   *
   * @param {Object} - column The column to check.
   */
  shouldDisplayColumnHeader: function(column) {
    // Is the column key in our column whitelist?
    return (
      this.props.columns && this.props.columns.indexOf(column) > -1
    );
  },


  /**
   * Sort the table by a column key. - Defaults to descending, will toggle to ascending.
   *
   * @param  {number} key the key fo the column to sort
   */
  sortByKey: function(key) {
    ContestActions.sortByKey(key);
  },


  render: function() {
    // Build up a list of rows to be dislayed.
    var visibleRows = this.props.data.map(function(row) {
      return (
        <Tr key={row.id} row={row} columns={this.props.columns} />
      );
    }.bind(this));

    // Infer table header titles from the keys of the first row object.
    var tableHeaders = (function() {
      if(this.props.data.length > 0) {

        return Object.keys(this.props.data[0]).map(function(column) {
          // Check if the column header should be displayed.
          if (this.shouldDisplayColumnHeader(column)) {
            // Use the supplied column header name, or fall back to the property key.
            var title = this.props.columnHeaders[column] || column;

            // Add css classes if the column is the actively sorted one.
            var cssClass = '';
            if (this.props.sortKey === column) {
              cssClass = 'active sort-' + this.props.sortDirection;
            }

            return (
              <th
                key={column}
                onClick={this.sortByKey.bind(this, column)}
                className={cssClass}
              >
                {title} <span className="table__sort-icon"></span>
              </th>
            );
          }

          return false;
        }.bind(this));

      } else{
        // If there are no rows, render nothing :(
        return '';
      }
    }.bind(this))();

    return (
      <table className="table">
        <thead>
          {tableHeaders}
        </thead>

        <tbody>
          {visibleRows}
        </tbody>
      </table>
    );
  }

});


module.exports = DataTable;
