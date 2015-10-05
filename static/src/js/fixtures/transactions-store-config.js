'use strict';

// match example: ```// 12-02-2015```
var DATE = /\d{2}-\d{2}-\d{4}/;


/**
 * match example: /?start_date=12-02-2014&end_date=12-05-2015
 * living it here as afterwards testing with correct filtering by dates will come
 */
var GET_PARAMS = new RegExp(
  /api\/transactions\//.source +
  /\?/.source +
  /start_date=/.source +
  DATE.source +
  /&/.source +
  /end_date=/.source +
  DATE.source
);

// everything that starts with history/
var TRANSACTION_DETAILS = /history\/.*/;


module.exports = [
  {
    pattern: '(.*)',

    fixtures: function(match, params, headers) {
      /**
       * Returns list of transactions if get params are in the format
       * provided in the GET_PARAMS regular expression
       */
      if (match[1].match(GET_PARAMS) !== null) {
        return require('./json/transactions-list.json');
      }

      /**
       * Returns detailed information about transaction
       */
      if (match[1].match(TRANSACTION_DETAILS) !== null) {
        return require('./json/transaction-details.json');
      }
    },

    /**
     * returns the result of the GET request
     *
     * @param match array Result of the resolution of the regular expression
     * @param data  mixed Data returns by `fixtures` attribute
     */
    get: function (match, data) {
      return {
        body: data
      };
    }

  }
];
