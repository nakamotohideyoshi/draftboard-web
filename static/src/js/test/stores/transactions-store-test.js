'use strict';

var request = require('superagent');
var expect = require('chai').expect;

var TransactionsActions = require('../../actions/transactions-actions');


describe("TransactionsStore", function() {

  before(function() {
    var fixtures = require('../../fixtures/transactions-store-config.js');

    this.TransactionsStore = require('../../stores/transactions-store.js');
    this.superagentMock = require('superagent-mock')(request, fixtures);
  });

  after(function() {
    this.superagentMock.unset();
  });

  afterEach(function() {
    this.TransactionsStore.resetData();
  });

  // it('getTransactions() with startDate and endDate should return fixture transactions', function() {
  //   var startDate = '25-12-2012';
  //   var endDate = '27-12-2015';
  //   TransactionsActions.getTransactions.trigger(startDate, endDate);
  //   expect(this.TransactionsStore.data.transactions.length).to.equal(5);
  // });

  it('transactionDetails() should populate the transactionDetails object in the store', function() {
    TransactionsActions.transactionDetails.trigger(1);
    expect(this.TransactionsStore.data.transactionDetails.pk).to.equal(1);
  });

});
