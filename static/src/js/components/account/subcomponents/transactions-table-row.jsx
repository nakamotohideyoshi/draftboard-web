import React from 'react';
// import * as AppActions from '../../../stores/app-state-store.js';
import moment from 'moment';
// Disable the transaction detail pane feature for now. We might add it
// back in at some point.
// require('./transactions-details.jsx');


const TransactionsTableRow = React.createClass({
  propTypes: {
    transaction: React.PropTypes.object.isRequired,
    focusTransaction: React.PropTypes.func.isRequired,
  },


  handleDetailsClick() {
    // Disable the transaction detail pane feature for now. We might add it
    // back in at some point.
    // this.props.focusTransaction(this.props.transaction.id);
    // event.preventDefault();
    // AppActions.openPane();
  },


  render() {
    return (
      <tr>
        <td>{moment(this.props.transaction.created).format('MM/DD/YYYY')}
          <sub className="table__sub">{moment(this.props.transaction.created).format('h:mm:ss a')}</sub>
        </td>
        <td>{this.props.transaction.details[0].amount}</td>
        <td>{this.props.transaction.description}</td>
        <td>{this.props.transaction.id}</td>
      </tr>
    );
  },
});


export default TransactionsTableRow;
