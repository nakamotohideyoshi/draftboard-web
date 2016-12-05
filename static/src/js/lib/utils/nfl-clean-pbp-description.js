/**
 * Clean up PBP description for NFL
 * - anything within parenthesis
 * - numbers before players
 * - anything after the first sentence
 * - replace ob with out
 * @param  {string} original From SportsRadar
 * @return {string}          Cleaned description
 */
export default (original) => {
  const regex = /\s*\([^\)]+\)\s*|\d+\-|(\.)\s[^\)]+/g;
  const replaced = original.replace(regex, '$1');

  // replace ob with out
  return replaced.replace(/(\sob\s)/g, ' out ');
};
