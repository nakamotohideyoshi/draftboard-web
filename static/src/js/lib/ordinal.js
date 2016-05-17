/**
 * Utility function to add ordinal suffixes to numbers.
 * via: https://gist.github.com/jlbruno/1535691
 *
 * ex:
 * ordinal(1) => 1st
 * ordinal(2) => 2nd
 * ordinal(3) => 3rd
 */
export default (num) => {
  const suffixes = ['th', 'st', 'nd', 'rd'];
  const v = num % 100;
  return num + (suffixes[(v - 20) % 10] || suffixes[v] || suffixes[0]);
};
