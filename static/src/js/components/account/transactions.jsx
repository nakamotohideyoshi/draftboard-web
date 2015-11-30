'use strict';

import React from 'react'
const ReactRedux = require('react-redux')
const store = require('../../store')
const renderComponent = require('../../lib/render-component')
import {fetchTransactions, filterTransactions } from '../../actions/transactions'

const TransactionsForm = require('./subcomponents/transactions-form.jsx');
const TransactionsTable = require('./subcomponents/transactions-table.jsx');

import { stringifyDate } from '../../lib/time.js';


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

  handlePeriodSelected({isPeriod = false, days=0, startDate=new Date(), endDate=new Date()}) {
    // if period is selected calling /?start_ts=[timestamp]&end_ts=[timestamp]/
    if (isPeriod) {
      const startDateString = stringifyDate(startDate, '-')
      const endDateString = stringifyDate(endDate, '-')
      const newUrl = window.location.pathname + "?from=" + startDateString + '&to=' + endDateString;
      window.history.pushState("change the", "url", newUrl)
    // if it is not period we are calling /?days=X api endpoint
    } else {
      const newUrl = window.location.pathname + "?since=" + days + "days"
      window.history.pushState("change the", "url", newUrl)
    }
    this.props.filterTransactions(isPeriod, days, startDate.getTime(), endDate.getTime())
  },

  render() {
    return (
      <div>
        <TransactionsForm onPeriodSelected={this.handlePeriodSelected}/>
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
    filterTransactions: (isPeriod, days, startDate, endDate) => dispatch(filterTransactions(isPeriod, days, startDate, endDate))
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
