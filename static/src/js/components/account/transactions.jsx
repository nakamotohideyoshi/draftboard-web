import React from 'react';
import { stringifyDate } from '../../lib/time.js';
import * as ReactRedux from 'react-redux';
import store from '../../store';
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
    fetchTransactions: () => dispatch(fetchTransactions()),
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
    this.props.fetchTransactions();
  },


  handleFocusTransaction(transactionId) {
    this.props.transactionFocused(transactionId);
  },


  handlePeriodSelected({ isPeriod = false, days = 0, startDate = new Date(), endDate = new Date() }) {
    // if period is selected calling /?start_ts=[timestamp]&end_ts=[timestamp]/
    if (isPeriod) {
      const startDateString = stringifyDate(startDate, '-');
      const endDateString = stringifyDate(endDate, '-');
      const newUrl = `${window.location.pathname}?from=${startDateString}&to=${endDateString}`;
      window.history.pushState('change the', 'url', newUrl);
    // if it is not period we are calling /?days=X api endpoint
    } else {
      const newUrl = `${window.location.pathname}?since=${days}days`;
      window.history.pushState('change the', 'url', newUrl);
    }
    this.props.filterTransactions(isPeriod, days, startDate.getTime(), endDate.getTime());
  },

  render() {
    return (
      <div>
        <TransactionsForm onPeriodSelected={this.handlePeriodSelected}/>
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


export default TransactionsConnected;
