'use strict';

var React = require('react');
var TransactionsTableRow = require('./transactions-table-row.jsx');


/**
 * Transactions table
 * By given array of transactions object renders them into table
 * and calculates summary informations as:
 *   - winnings
 *   - contesnts
 *   - cashes
 *   - transactions count
 * that is calculated with javascript
 */
var TransactionsTable = React.createClass({

  propTypes: {
    transactions: React.PropTypes.array.isRequired
  },

  render: function() {
    var transactionsWinnings = '$3,234.50';
    var transactionsContests = '425';
    var transactionsCashed = '123';
    var transactionsCount = '1,231';

    var transactionsRows = this.props.transactions.map(function(transaction) {
      return (
        <TransactionsTableRow
          key={transaction.pk}
          transaction={transaction} />
      );
    }.bind(this));

    return (
      <div id="transactions-listed-table">
        <div className="table-summary">
          <div className="table-summary--item">
            <span className="table-summary--label">Winnings</span>{transactionsWinnings}
          </div>

          <div className="table-summary--item">
            <span className="table-summary--label">Contests</span>{transactionsContests}
          </div>

          <div className="table-summary--item">
            <span className="table-summary--label">Cashes</span>{transactionsCashed}
          </div>

          <div className="table-summary--item">
            <span className="table-summary--label">Transactions</span>{transactionsCount}
          </div>
        </div>

        <table className="table table--zebra">
          <thead>
            <tr>
              <th>Date</th>
              <th>Amount</th>
              <th>Balance</th>
              <th>Type</th>
              <th>Description</th>
              <th>Details</th>
            </tr>
          </thead>

          <tbody>
            {transactionsRows}
          </tbody>
        </table>
      </div>
    );
  }
});


module.exports = TransactionsTable;
