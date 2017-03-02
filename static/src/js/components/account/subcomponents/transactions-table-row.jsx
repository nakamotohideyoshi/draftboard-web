import React from 'react';
import { humanizeCurrency } from '../../../lib/utils/currency';
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
        <td>{moment(this.props.transaction.details.created).format('MM/DD/YYYY')}
          <sub className="table__sub">{moment(this.props.transaction.details.created).format('h:mm:ss a')}</sub>
        </td>
        <td>{humanizeCurrency(this.props.transaction.details[0].amount)}</td>
        <td>{this.props.transaction.description}</td>
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
