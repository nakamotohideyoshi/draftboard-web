import { expect } from 'chai';

import { humanizeCurrency } from '../../../lib/utils/currency';


describe('utils.colors.humanizeCurrency', () => {
  it('should return $0 if amount is 0', () => {
    expect(humanizeCurrency(0.00)).to.equal('$0');
  });

  it('should return with no decimal points with $ if whole number', () => {
    expect(humanizeCurrency(20)).to.equal('$20');
  });

  it('should return with two decimal points with $ if not 0', () => {
    expect(humanizeCurrency(20.20, false)).to.equal('$20.20');
  });

  it('should return with comma if larger than 1000', () => {
    expect(humanizeCurrency(12020.20, false)).to.equal('$12,020.20');
  });
});
