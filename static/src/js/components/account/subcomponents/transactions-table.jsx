import React from 'react';
import TransactionsTableRow from './transactions-table-row.jsx';


const TransactionsTable = (props) => {
  const transactionsRows = props.transactions.map((transaction) =>
    <TransactionsTableRow
      key={transaction.id}
      transaction={transaction}
      focusTransaction={props.focusTransaction}
    />
  );

  return (
    <div id="transactions-listed-table">
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
