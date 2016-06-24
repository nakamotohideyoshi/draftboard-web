import { expect } from 'chai';

import { percentageHexColor } from '../../../lib/utils/colors';


describe('utils.colors.percentageHexColor', () => {
  it('should generate same hex if the start and end are the same', () => {
    expect(percentageHexColor('ffffff', 'ffffff', 50)).to.equal('ffffff');
  });

  it('should return start if percentage is 0', () => {
    expect(percentageHexColor('ffffff', 'dddddd', 0)).to.equal('ffffff');
  });

  it('should return end if percentage is 100', () => {
    expect(percentageHexColor('ffffff', 'dddddd', 1)).to.equal('dddddd');
  });

  it('should generate hex halfway between if percentage is 0.5', () => {
    expect(percentageHexColor('ffffff', 'dddddd', 0.5)).to.equal('eeeeee');
  });
});
