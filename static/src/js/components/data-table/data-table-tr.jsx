'use strict';

var React = require('react');
var Td = require('../data-table/data-table-td.jsx');
var TrMixin = require('../data-table/data-table-tr-mixin.jsx');


/**
 * Render a single DataTable table row.
 *
 * @param {Object} row - A single row of the DataTable's data.
 * @param {array} columns - The columns that should be displayed. This is directly passed down
 * through DataTable.
 */
var DataTableTr = React.createClass({
  mixins: [TrMixin],


  propTypes: {
    row: React.PropTypes.object.isRequired,
    columns: React.PropTypes.array
  },


  render: function() {
    var cells = [];

    // Loop through the row's propeties and create TD's from them.
    for (var prop in this.props.row) {
      if(this.shouldDisplayColumn(prop)) {
        if (this.props.row.hasOwnProperty(prop)) {
          cells.push(<Td key={this.props.row[prop]} cellName={prop} cellData={this.props.row[prop]} />);
        }
      }
    }

    return (
      <tr key={this.props.row.id}>
        {cells}
      </tr>
    );
  }

});


module.exports = DataTableTr;
