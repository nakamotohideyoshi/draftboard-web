/**
 * BEM helper to generate block and its modifiers
 * @param  {string} block     Block name, `my-block`
 * @param  {array} modifiers  Array of modifiers, `['modifier1', 'modifier2', ...]`
 * @return {string}           Generated classnames, `my-block my-block--modifier1 my-block--modifier2`
 */
export const generateBlockNameWithModifiers = (block, modifiers = []) =>
  modifiers.reduce((sum, modifier) => `${block}--${modifier} ${sum}`, block);
