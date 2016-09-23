import { expect } from 'chai';

import { humanizeFP } from '../../../lib/utils/numbers';


describe('utils.numbers.humanizeFP', () => {
  it('should return fp untouched if string', () => {
    expect(humanizeFP('10.00')).to.equal('10.00');
  });

  it('should return 0 if FP equals 0', () => {
    expect(humanizeFP(0.00, true)).to.equal('0');
  });

  it('should return whole number if FP equals 1.00', () => {
    expect(humanizeFP(1.00)).to.equal('1');
  });

  it('should return hundredths if FP is decimal', () => {
    expect(humanizeFP(1.02)).to.equal('1.02');
  });

  it('should return +- if showPlusMinus is true', () => {
    expect(humanizeFP(1, true)).to.equal('+1');

    // make sure there's an extra space in there, silly font
    expect(humanizeFP(-1, true)).to.equal('- 1');
  });
});
