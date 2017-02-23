import React from 'react';
import { stringifyDate } from '../../lib/time.js';
import log from '../../lib/logging.js';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import { querystring } from '../../lib/utils';
import renderComponent from '../../lib/render-component';
import { transactionFocused, fetchTransactions, filterTransactions } from '../../actions/transactions';

const TransactionsForm = require('./subcomponents/transactions-form.jsx');
const TransactionsTable = require('./subcomponents/transactions-table.jsx');
const { Provider, connect } = ReactRedux;


function mapStateToProps(state) {
  return {
    transactions: state.transactions.filteredTransactions,
    filters: state.transactions.filters,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    fetchTransactions: (startDate, endDate) => dispatch(fetchTransactions(startDate, endDate)),
    filterTransactions: (isPeriod, days, startDate, endDate) => dispatch(
      filterTransactions(isPeriod, days, startDate, endDate)
    ),
    transactionFocused: (transactionId) => dispatch(transactionFocused(transactionId)),
  };
}


const Transactions = React.createClass({

  propTypes: {
    transactions: React.PropTypes.array.isRequired,
    filters: React.PropTypes.object.isRequired,
    fetchTransactions: React.PropTypes.func.isRequired,
    filterTransactions: React.PropTypes.func.isRequired,
    transactionFocused: React.PropTypes.func.isRequired,
  },


  componentWillMount() {
    const qs = querystring();
    const fromTo = window.location.search;
    let endDate = new Date();
    let startDate = new Date().setMonth(endDate.getMonth() - 1);

    if (fromTo === '') {
      this.props.fetchTransactions(startDate, endDate.getTime());
    } else {
      // Grab dates from  url params and  convert to actual Dates, then fetch transactions.
      endDate = new Date(qs.to);
      startDate = new Date(qs.from);
      if (!isNaN(startDate) && !isNaN(endDate)) {
        this.props.fetchTransactions(startDate.getTime(), endDate.getTime());
      } else {
        log.warn('Invalid date provided!')
      }
    }
  },


  handleFocusTransaction(transactionId) {
    this.props.transactionFocused(transactionId);
  },


  handlePeriodSelected({
    isPeriod = false, days = 0, startDate = new Date(), endDate = new Date(),
  }) {
    let start = startDate;
    let end = endDate;

    //  Is this a Moment.js date? if so, convert them to native Date objects.
    if (typeof start.format === 'function') {
      start = start.toDate();
    }
    if (typeof end.format === 'function') {
      end = end.toDate();
    }

    // If the same date was passed in, make the start 1 month ago.
    if (startDate === end) {
      startDate.setMonth(end.getMonth() - 1);
    }

    // if period is selected calling /?start_ts=[timestamp]&end_ts=[timestamp]/
    if (isPeriod) {
      const startDateString = stringifyDate(start, '-');
      const endDateString = stringifyDate(end, '-');
      const newUrl = `${window.location.pathname}?from=${startDateString}&to=${endDateString}`;
      window.history.pushState('change the', 'url', newUrl);
    // if it is not period we are calling /?days=X api endpoint
    } else {
      const newUrl = `${window.location.pathname}?since=${days}days`;
      window.history.pushState('change the', 'url', newUrl);
    }

    // this.props.filterTransactions(isPeriod, days, startDate.getTime(), endDate.getTime());
    this.props.fetchTransactions(start.getTime(), end.getTime());
  },

  render() {
    return (
      <div>
        <TransactionsForm onPeriodSelected={this.handlePeriodSelected} />
        <TransactionsTable
          transactions={this.props.transactions}
          focusTransaction={this.handleFocusTransaction}
        />
      </div>
    );
  },
});


const TransactionsConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Transactions);


renderComponent(
  <Provider store={store}>
    <TransactionsConnected />
  </Provider>,
  '#account-transactions'
);


module.exports = TransactionsConnected;
