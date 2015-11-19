'use strict';


var Reflux = require('reflux');
var TransactionsActions = require('../actions/transactions-actions');
var log = require('../lib/logging');
var request = require('superagent');

// should become '/api/transactions/' afterwards
var API_BASE = '/account/api/transactions/';


var TransactionsStore = Reflux.createStore({
  data: {},

  init: function() {
    this.listenTo(TransactionsActions.getTransactions, this.onGetTransactions);
    this.listenTo(TransactionsActions.transactionDetails, this.onTransactionDetails);

    this.data = {
      'transactions': [],
      'transactionDetails': {}
    };
  },

  resetData: function() {
    this.data = {
      'transactions': [],
      'transactionDetails': {}
    };
  },

  // this works with startDate and endDate as get params
  onGetTransactions: function(startDate, endDate) {
    log.debug('TransactionsStore.onGetTransactions()');

    request
      .get(API_BASE)
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .query({start_date: startDate, end_date: endDate})
      .end(function(err, res) {
        if(err) {
          log.error(err);
          TransactionsActions.getTransactions.failed();
        } else {
          this.data.transactions = res.body;
          this.trigger(this.data);
          TransactionsActions.getTransactions.completed();
        }
      }.bind(this));
  },

  onTransactionDetails: function(pk) {
    log.debug('TransactionsStore.onTransactionDetails()');
    // if same transaction that is in the data is required, don't send request
    if (this.data.transactionDetails.pk === pk) {
      this.trigger(this.data);
      TransactionsActions.transactionDetails.completed();
      return;
    }

    request
      .get(API_BASE  + 'history/')
      .set({'X-REQUESTED-WITH': 'XMLHttpRequest'})
      .end(function(err, res) {
        if(err) {
          log.error(err);
          TransactionsActions.transactionDetails.failed();
        } else {
          this.data.transactionDetails = res.body;
          this.trigger(this.data);
          TransactionsActions.transactionDetails.completed();
        }
      }.bind(this));
  }

});


module.exports = TransactionsStore;
