'use strict';

import React from 'react';
const renderComponent = require('../../../lib/render-component');
import * as AppActions from '../../../stores/app-state-store.js'

const TransactionsDetails = require('./transactions-details.jsx');


const TransactionsTableRow = React.createClass({

  propTypes: {
    transaction: React.PropTypes.object.isRequired
  },

  handleShowDetails(event) {
    event.preventDefault()
    renderComponent(<TransactionsDetails transaction={this.props.transaction} />, '.pane__content')
    AppActions.openPane()
  },

  render() {
    return (
      <tr>
        <td>{this.props.transaction.date_date} <sub className="table__sub">{this.props.transaction.date_time}</sub></td>
        <td>{this.props.transaction.amount}</td>
        <td>{this.props.transaction.balance}</td>
        <td>{this.props.transaction.type}</td>
        <td>{this.props.transaction.description}</td>
        <td><a classNameName="transaction-info" onClick={this.handleShowDetails} href="#">{this.props.transaction.pk}</a></td>
      </tr>
    );
  }

});


export default TransactionsTableRow;
