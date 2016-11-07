/**
 * Adding commas to numbers by thousands
 * @param  {number} x Amount
 * @return {string}   Formatted string
 */
const numberWithCommas = (x) => {
  const parts = x.toString().split('.');
  parts[0] = parseInt(parts[0], 10).toLocaleString('en');
  return parts.join('.');
};

/**
 * Shortcut for humanizing currency
 * - $0 for 0
 * - if noCentsOnWholeAmount is true and amount is whole, return `$2` for 2
 * - anything else in hundredths, eg `$20.00`
 * - adds commas for larger numbers, eg `$12,080.20`
 * @param  {number} amount               How much to humanize
 * @param {boolean} noCentsOnWholeAmount (optional) do you want to have cents on a whole dollar amount?
 * @return {string}                      Amount with $
 */
export const humanizeCurrency = (amount, noCentsOnWholeAmount = true) => {
  // so we can have null passed through
  if (typeof amount !== 'number') return amount;

  if (amount <= 0 && parseInt(amount, 10) === 0) return '$0';
  if (noCentsOnWholeAmount && amount % 1 === 0) return `$${parseInt(amount, 10)}`;

  const amountRoundedToHundredth = (parseInt(amount * 100, 10) / 100).toFixed(2);

  return `$${numberWithCommas(amountRoundedToHundredth)}`;
};
