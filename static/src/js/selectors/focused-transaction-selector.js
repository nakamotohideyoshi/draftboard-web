import { createSelector } from 'reselect';
import find from 'lodash/find';


const allTransactionsSelector = (state) => state.transactions.allTransactions;
const focusedTransactionIdSelector = (state) => state.transactions.focusedTransactionId;


/**
 * Select the currently focused transaction - to be displayed in the sidebar of
 * the accounts - transactions page.
 */
export const focusedTransactionSelector = createSelector(
  allTransactionsSelector, focusedTransactionIdSelector,
  (transactions, focusedTransactionId) => {
    if (focusedTransactionId) {
      return find(transactions, { id: focusedTransactionId });
    }

    return {};
  }
);
