"use strict";

var React = require('react');
var Reflux = require('reflux');
var renderComponent = require('../../lib/render-component');

var TransactionsActions = require('../../actions/transactions-actions');
var TransactionsStore = require('../../stores/transactions-store');

var TransactionsForm = require('./subcomponents/transactions-form.jsx');
var TransactionsTable = require('./subcomponents/transactions-table.jsx');


/**
 * The transactions section from the account/settings page
 *
 * TODO:
 * - not to refresh page
 */
var Transactions = React.createClass({

  mixins: [
    Reflux.connect(TransactionsStore)
  ],

  getInitialState: function() {
    // get transactions based on document.url (for get params)
    TransactionsActions.getTransactions();
    return {
      'transactions': TransactionsStore.data.transactions
    };
  },

  /**
   * Call the action that will reupdate the store
   * @param  {moment Object} startDate [description]
   * @param  {moment Object} endDate   [description]
   */
  getTransactions: function(startDate, endDate) {
    if (startDate !== null && endDate !== null) {
      // populate the get params withouth invoking page refresh
      var startDateString = startDate.format('MM-DD-YYYY');
      var endDateString = endDate.format('MM-DD-YYYY');
      var newUrl = window.location.pathname + "?from=" + startDateString + '&to=' + endDateString;
      window.history.pushState("dummy", "javascript..", newUrl);

      TransactionsActions.getTransactions(startDate, endDate);
    }
  },

  render: function() {
    return (
      <div>
        <TransactionsForm onPeriodSelected={this.getTransactions}/>
        <TransactionsTable transactions={this.state.transactions} />
      </div>
    );
  }
});


renderComponent(<Transactions />, '#account-transactions');


module.exports = Transactions;
