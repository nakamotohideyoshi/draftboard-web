import React from 'react';
import * as AppActions from '../../../stores/app-state-store.js';
require('./transactions-details.jsx');


const TransactionsTableRow = React.createClass({
  propTypes: {
    transaction: React.PropTypes.object.isRequired,
    focusTransaction: React.PropTypes.func.isRequired,
  },


  handleDetailsClick(event) {
    this.props.focusTransaction(this.props.transaction.pk);
    event.preventDefault();
    AppActions.openPane();
  },


  render() {
    return (
      <tr>
        <td>{this.props.transaction.date_date} <sub className="table__sub">{this.props.transaction.date_time}</sub></td>
        <td>{this.props.transaction.amount}</td>
        <td>{this.props.transaction.balance}</td>
        <td>{this.props.transaction.type}</td>
        <td>{this.props.transaction.description}</td>
        <td>
          <a
            classNameName="transaction-info"
            onClick={this.handleDetailsClick}
            href="#"
          >
            {this.props.transaction.pk}
        </a>
        </td>
      </tr>
    );
  },
});


export default TransactionsTableRow;
