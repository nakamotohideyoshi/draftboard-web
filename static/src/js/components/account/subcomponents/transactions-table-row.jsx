'use strict';

var React = require('react');
var renderComponent = require('../../../lib/render-component');
// var AppAction = require('../../../actions/app-actions');
import * as AppActions from '../../../stores/app-state-store.js'
var TransactionsDetails = require('./transactions-details.jsx');

/**
 * Component representing a single row from the table with transactions
 */
var TransactionsTableRow = React.createClass({

  propTypes: {
    transaction: React.PropTypes.object.isRequired
  },

  /**
   * Prevent the default href acction and invoke openning of the side pane
   * Render the TransactionsDetails component inside the .pane__content
   */
  showDetails: function() {
    // render the transactionDetail component inside THAT PANE.
    renderComponent(<TransactionsDetails transaction={this.props.transaction} />, '.pane__content');
    AppActions.openPane();
  },

  render: function() {
    return (
      <tr>
        <td>{this.props.transaction.date_date} <sub className="table__sub">{this.props.transaction.date_time}</sub></td>
        <td>{this.props.transaction.amount}</td>
        <td>{this.props.transaction.balance}</td>
        <td>{this.props.transaction.type}</td>
        <td>{this.props.transaction.description}</td>
        <td><a classNameName="transaction-info" onClick={this.showDetails} href="#">{this.props.transaction.pk}</a></td>
      </tr>
    );
  }

});


module.exports = TransactionsTableRow;
