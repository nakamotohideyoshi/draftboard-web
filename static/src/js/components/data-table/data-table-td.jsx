'use strict';

var React = require('react');


/**
 * Renders a single <td> in a DataTable
 *
 * @param {node} cellData - A single <td> of data.
 * @param {string} CellName - The key of the element in the data object.
 */
var DataTableTd = React.createClass({
  propTypes: {
    cellName: React.PropTypes.string.isRequired,
    cellData: React.PropTypes.node.isRequired
  },

  render: function() {
    return (
      <td className={'cell-' + this.props.cellName}>{this.props.cellData}</td>
    );
  }

});


module.exports = DataTableTd;
