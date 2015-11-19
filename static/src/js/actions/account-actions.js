'use strict';

var Reflux = require('reflux');

var AccountActions = Reflux.createActions({

  'userBaseInfo': {children: ['completed', 'failed']},
  'userExtraInfo': {children: ['completed', 'failed']},
  'updateBaseInfo': {children: ['completed', 'failed']},
  'updateExtraInfo': {children: ['completed', 'failed']},

  'deposit': {children: ['completed', 'failed']},
  'withdraw': {children: ['completed', 'failed']},
  'addPaymentMethod': {children: ['completed', 'failed']},
  'getPaymentMethods': {children: ['completed', 'failed']},
  'removePaymentMethod': {children: ['completed', 'failed']},
  'setDefaultPaymentMethod': {children: ['completed', 'failed']}

});


module.exports = AccountActions;
