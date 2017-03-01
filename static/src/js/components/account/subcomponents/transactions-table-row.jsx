import React from 'react';
import * as AppActions from '../../../stores/app-state-store.js';
import moment from 'moment';
require('./transactions-details.jsx');


const TransactionsTableRow = React.createClass({
  propTypes: {
    transaction: React.PropTypes.object.isRequired,
    focusTransaction: React.PropTypes.func.isRequired,
  },


  handleDetailsClick(event) {
    this.props.focusTransaction(this.props.transaction.id);
    event.preventDefault();
    AppActions.openPane();
  },


  render() {
    return (
      <tr>
        <td>{moment(this.props.transaction.details[0].created).format('MM/DD/YYYY')}
          <sub className="table__sub">{moment(this.props.transaction.details[0].created).format('h:mm:ss a')}</sub>
        </td>
        <td>{this.props.transaction.details[0].amount}</td>
        <td>{this.props.transaction.details[0].balance}</td>
        <td>{this.props.transaction.type}</td>
        <td>{this.props.transaction.details[0].category.description}</td>
        <td>
          <a
            className="transaction-info"
            onClick={this.handleDetailsClick}
            href="#"
          >
            {this.props.transaction.id}
        </a>
        </td>
      </tr>
    );
  },
});


export default TransactionsTableRow;
