'use strict';

/**
  * sample data in store:

  this.data = {
   'user': {
      'username': 'fancyusername',
      'email': 'example@dfs.com',
      'balance': '23130.00',
      'bonus': '3130.00',
      'mailNotifications': {
        'contests_starting': true,
        'contests_victories': true,
        'contests_upcoming': true,
        'newsletters': false
      }
    },

    'information': {
      'name': 'Lookma Noname',
      'address1': 'Some address or should it',
      'address2': 'Be connected with specific payment method',
      'city': 'Denver',
      'state': 'Colorado',
      'stateShort': 'CO',
      'zipcode': '4000'
    },

    'paymentMethods': [
      {
        'type': 'visa',
        'ending': 2785,
        'expires': '11/2016',
        'default': false,
        'id': 1,
      },
      {
        'type': 'amex',
        'ending': 2785,
        'expires': '11/2016',
        'default': true,
        'id': 2,
      },
      {
          'type': 'discover',
          'ending': 2785,
          'expires': '11/2016',
          'default': false,
          'id': 3,
      },
      {
          'type': 'mastercard',
          'ending': 2785,
          'expires': '11/2016',
          'default': false,
          'id': 4,
      },

      // if errors from the backend are present
      'userFormErrors': {},
      'informationFormErrors': {},
      'addPaymentMethodFormErrors': {}
    ]
  };
*/

var Reflux = require('reflux');
var AccountActions = require('../actions/account-actions');
var request = require('superagent');
require('superagent-django-csrf');
var log = require("../lib/logging");
// TODO: import only what is needed from lodash
var _ = require('lodash');

// should become '/api/account/' afterwards
var API_BASE = '/account/api/account/';


var AccountStore = Reflux.createStore({
  data: {},

  init: function() {
    this.listenTo(AccountActions.userBaseInfo, this.onUserBaseInfo);
    this.listenTo(AccountActions.userExtraInfo, this.onUserExtraInfo);
    this.listenTo(AccountActions.updateBaseInfo, this.onUpdateBaseInfo);
    this.listenTo(AccountActions.updateExtraInfo, this.onUpdateExtraInfo);

    this.listenTo(AccountActions.deposit, this.onDeposit);
    this.listenTo(AccountActions.withdraw, this.onWithdraw);
    this.listenTo(AccountActions.addPaymentMethod, this.onAddPaymentMethod);
    this.listenTo(AccountActions.getPaymentMethods, this.onGetPaymentMethods);
    this.listenTo(AccountActions.removePaymentMethod, this.onRemovePaymentMethod);
    this.listenTo(AccountActions.setDefaultPaymentMethod, this.onSetDefaultPaymentMethod);

    this.data = {
      'user': {},
      'information': {},
      'paymentMethods': [],
      'userFormErrors': {},
      'informationFormErrors': {},
      'depositFormErrors': {},
      'withdrawFormErrors': {},
      'addPaymentMethodFormErrors': {}
    };
  },

  resetData: function() {
    this.data = {
      'user': {},
      'information': {},
      'paymentMethods': [],
      'userFormErrors': {},
      'informationFormErrors': {},
      'depositFormErrors': {},
      'withdrawFormErrors': {},
      'addPaymentMethodFormErrors': {}
    };
  },

  /**
   * Get basic user info that is email / username and email notifications
   * this populate this.data.user object
   * if force is set to false, and this.data.user is not Empty object, don't do API call
   */
  onUserBaseInfo: function(force) {
    log.debug('AccountStore.onUserBaseInfo()');
    if (force !== undefined && force === false && !_.isEmpty(this.data.user)) {
      return;
    }

    request
      .get(API_BASE + 'user/')
      .set({'X-REQUESTED-WITH': 'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if (err) {
          log.error(err);
          AccountActions.userBaseInfo.failed();
        } else {
          this.data.user = res.body;
          this.trigger(this.data);
          AccountActions.userBaseInfo.completed();
        }
      }.bind(this));
  },

  /**
   * Get extra info connected with the user
   * addresses for the payment methods
   * birth date
   * state / city / zipcode
   */
  onUserExtraInfo: function() {
    log.debug('AccountStore.onUserExtraInfo()');
    request
      .get(API_BASE + 'information/')
      .set({'X-REQUESTED-WITH': 'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if (err) {
          log.error(err);
          AccountActions.userExtraInfo.failed();
        } else {
          this.data.information = res.body;
          this.trigger(this.data);
          AccountActions.userExtraInfo.completed();
        }
      }.bind(this));
  },

  /**
   * When user tries to update password / email notifications / email
   * will take dictlike / object parameters for the post data
   * on errors populate this.data.userFormErrors
   * otherwise update with javascript this.data.user directly
   */
  onUpdateBaseInfo: function(callback) {
    log.debug('AccountStore.onUpdateBaseInfo()');
    request
      .post(API_BASE + 'user/')
      .send({})
      .end(function(err, res) {
        if (err) {
          log.error(err);
          if ('errors' in res.body) {
            this.data.userFormErrors = res.body.errors;
          }
          AccountActions.updateBaseInfo.failed();
        } else {
          // this.data.user = res.body;
          this.data.userFormErrors = {};
          AccountActions.updateBaseInfo.completed();
        }

        this.trigger(this.data);
        if (callback !== undefined) {
          callback();
        }
      }.bind(this));
  },

  /**
   * When use tries to update address / zip code / city / state / etc.
   * will take dictlike / object parameters for the post data
   * on errors populate this.data.informationFormErrors
   * otherwise update with javascript this.data.information directly
   */
  onUpdateExtraInfo: function(callback) {
    log.debug('AccountStore.onUpdateExtraInfo()');
    request
      .post(API_BASE + 'information/')
      .send({})
      .end(function(err, res) {
        if (err) {
          log.error(err);
          if ('errors' in res.body) {
            this.data.informationFormErrors = res.body.errors;
          }
          AccountActions.updateExtraInfo.failed();
        } else {
          this.data.informationFormErrors = {};
          AccountActions.updateExtraInfo.completed();
        }

        this.trigger(this.data);
        if (callback !== undefined) {
          callback();
        }
      }.bind(this));
  },

  /**
   * Gets payment methods connected with the user
   */
  onGetPaymentMethods: function() {
    log.debug('AccountStore.onGetPaymentMethods()');
    request
      .get(API_BASE + 'payments/')
      .set({'X-REQUESTED-WITH': 'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if (err) {
          log.error(err);
          AccountActions.getPaymentMethods.failed();
        } else {
          this.data.paymentMethods = res.body;
          this.trigger(this.data);
          AccountActions.getPaymentMethods.completed();
        }
      }.bind(this));
  },

  /**
   * Invoked when user wants to deposit some money
   * will take "amount" parameter later
   * and will update user balance straight away
   */
  onDeposit: function() {
    log.debug('AccountStore.onDeposit()');
    request
      .post(API_BASE + 'payments/deposit/')
      .send({})
      .end(function(err, res) {
        if (err) {
          log.error(err);
          if ('errors' in res.body) {
            this.data.depositFormErrors = res.body.errors;
          }
          AccountActions.deposit.failed();
        } else {
          this.trigger(this.data);
          AccountActions.deposit.completed();
        }
      }.bind(this));
  },

  /**
   * Invoked when user tries to withdraw some amount
   * will take "amount" parameter later
   * and will update user balance straight away
   */
  onWithdraw: function() {
    log.debug('AccountStore.onWithdraw()');
    request
      .post(API_BASE + 'payments/withdraw/')
      .send({})
      .end(function(err, res) {
        if (err) {
          log.error(err);
          if ('errors' in res.body) {
            this.data.withdrawFormErrors = res.body.errors;
          }
          AccountActions.withdraw.failed();
        } else {
          AccountActions.withdraw.completed();
        }
        this.trigger(this.data);
      }.bind(this));
  },

  /**
   * Add new payment method:
   * If backend returns json with 'errors' in it populate this.data.addPaymentMethodFormErrors
   * otherwise (on 201 / 202 response for example), simply insert the new payment method
   * in this.data.paymentMethods
   */
  onAddPaymentMethod: function() {
    log.debug('AccountStore.onAddPaymentMethod()');
    request
      .post(API_BASE + 'payments/add/')
      .send({})
      .end(function(err, res) {
        if (err) {
          log.error(err);
          AccountActions.addPaymentMethod.failed();
        } else {
          if ('errors' in res.body) {
            this.data.addPaymentMethodFormErrors = res.body.errors;
          }
          this.trigger(this.data);
          AccountActions.addPaymentMethod.completed();
        }
      }.bind(this));
  },

  /**
   * By given payment method pk, remove it
   * if status is 204, remove it with JS from the paymentMethods lists in the data
   */
  onRemovePaymentMethod: function(pk) {
    log.debug('AccountStore.onRemovePaymentMethod()');
    request
      .del(API_BASE + 'payments/remove/' + '1' + '/')
      .end(function(err) {
        if (err) {
          log.error(err);
          AccountActions.removePaymentMethod.failed();
        } else {
          _.remove(this.data.paymentMethods, function(method) {
            return method.id === pk;
          });

          this.trigger(this.data);
          AccountActions.removePaymentMethod.completed();
        }
      }.bind(this));
  },

  /**
   * By given payment method pk, change it to be the default
   * if status is 201, update this.data.paymetnMethods list directly with javascript
   */
  onSetDefaultPaymentMethod: function(pk) {
    log.debug('AccountStore.onSetDefaultPaymentMethod()');
    request
      .post(API_BASE + 'payments/setdefault/')
      .end(function(err) {
        if (err) {
          log.error(err);
          AccountActions.setDefaultPaymentMethod.failed();
        } else {
          _.map(this.data.paymentMethods, function(method) {
            if (method.id === pk) {
              method['default'] = true;
            } else {
              method['default'] = false;
            }
          });

          this.trigger(this.data);
          AccountActions.setDefaultPaymentMethod.completed();
        }
      }.bind(this));
  }

});


module.exports = AccountStore;
