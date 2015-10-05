'use strict';

var Reflux = require('reflux');


var TransactionsActions = Reflux.createActions({

  'getTransactions': {children: ['completed', 'failed']},
  'transactionDetails': {children: ['completed', 'failed']}

});


module.exports = TransactionsActions;
