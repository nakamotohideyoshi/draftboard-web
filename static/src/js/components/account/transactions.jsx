'use strict';

import React from 'react'
const ReactRedux = require('react-redux')
const store = require('../../store')
const renderComponent = require('../../lib/render-component')
import {fetchTransactions, filterTransactions } from '../../actions/transactions'

const TransactionsForm = require('./subcomponents/transactions-form.jsx');
const TransactionsTable = require('./subcomponents/transactions-table.jsx');


const Transactions = React.createClass({

  propTypes: {
    transactions: React.PropTypes.array.isRequired,
    filters: React.PropTypes.object.isRequired,
    fetchTransactions: React.PropTypes.func.isRequired,
    filterTransactions: React.PropTypes.func.isRequired
  },

  componentWillMount() {
    this.props.fetchTransactions()
  },

  handleFilterChange(startDate, endDate) {
    // var startDateString = startDate.format('MM-DD-YYYY');
    // var endDateString = endDate.format('MM-DD-YYYY');
    // var newUrl = window.location.pathname + "?from=" + startDateString + '&to=' + endDateString;
    // window.history.pushState("dummy", "javascript..", newUrl);
    this.props.filterTransactions(startDate, endDate)
  },

  render() {
    return (
      <div>
        <TransactionsForm onPeriodSelected={this.handleFilterChange}/>
        <TransactionsTable transactions={this.props.transactions} />
      </div>
    );
  }
});


let {Provider, connect} = ReactRedux;

function mapStateToProps(state) {
  return {
    transactions: state.transactions.filteredTransactions,
    filters: state.transactions.filters
  };
}

function mapDispatchToProps(dispatch) {
  return {
    fetchTransactions: () => dispatch(fetchTransactions()),
    filterTransactions: (startDate, endDate) => dispatch(filterTransactions(startDate, endDate))
  };
}


var TransactionsConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Transactions);


renderComponent(
  <Provider store={store}>
    <TransactionsConnected />
  </Provider>,
  '#account-transactions'
);


export default TransactionsConnected;
