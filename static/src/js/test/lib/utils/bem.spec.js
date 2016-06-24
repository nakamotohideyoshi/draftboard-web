import { expect } from 'chai';

import { generateBlockNameWithModifiers } from '../../../lib/utils/bem';


describe('utils.bem.generateBlockNameWithModifiers', () => {
  it('should return only block if there are no modifiers', () => {
    expect(generateBlockNameWithModifiers('my-block', [])).to.equal('my-block');
  });

  it('should return block and modifiers normally', () => {
    expect(generateBlockNameWithModifiers('my-block', ['modifier1', 'modifier2']))
      .to.equal('my-block--modifier2 my-block--modifier1 my-block');
  });
});
