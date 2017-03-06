import React from 'react';
import TransactionsTableRow from './transactions-table-row.jsx';


const TransactionsTable = (props) => {
  // TODO: to be calculated in runtime
  const transactionsWinnings = '$3,234.50';
  const transactionsContests = '425';
  const transactionsCashed = '123';
  const transactionsCount = '1,231';

  const transactionsRows = props.transactions.map((transaction) =>
    <TransactionsTableRow
      key={transaction.id}
      transaction={transaction}
      focusTransaction={props.focusTransaction}
    />
  );

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
            <th>Description</th>
            <th>Transaction ID</th>
          </tr>
        </thead>

        <tbody>
          {transactionsRows}
        </tbody>
      </table>
    </div>
  );
};

TransactionsTable.propTypes = {
  transactions: React.PropTypes.array.isRequired,
  focusTransaction: React.PropTypes.func.isRequired,
};

module.exports = TransactionsTable;
