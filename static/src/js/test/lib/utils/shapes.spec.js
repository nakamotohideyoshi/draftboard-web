import { expect } from 'chai';
import { describeArc, polarToCartesian } from '../../../lib/utils/shapes';


describe('utils.shapes.polarToCartesian', () => {
  it('should have (0, -1) for 0,0 origin, 1 radius, 0deg', () => {
    const c = polarToCartesian(0, 0, 1, 0);
    expect(c.x).to.equal(0);
    expect(c.y).to.equal(-1);
  });

  it('should have (1, 0) for 0,0 origin, 1 radius, 90deg', () => {
    const c = polarToCartesian(0, 0, 1, 90);
    expect(c.x).to.equal(1);
    expect(c.y).to.equal(0);
  });

  it('should have (0, 1) for 0,0 origin, 1 radius, 180deg', () => {
    const c = polarToCartesian(0, 0, 1, 180);
    expect(c.x).to.equal(0);
    expect(c.y).to.equal(1);
  });

  it('should have (-1, 0) for 0,0 origin, 1 radius, 270deg', () => {
    const c = polarToCartesian(0, 0, 1, 270);
    expect(c.x).to.equal(-1);
    expect(c.y).to.equal(0);
  });

  it('should have same result for 0 as 360, as we use modulus', () => {
    const c = polarToCartesian(0, 0, 1, 360);
    expect(c.x).to.equal(0);
    expect(c.y).to.equal(-1);
  });
});


describe('utils.shapes.describeArc', () => {
  it('should match result if start to end is 0deg', () => {
    expect(describeArc(0, 0, 1, 0, 0)).to.equal('M 0 -1 A 1 1 0 0 0 0 -1');
  });

  it('should match result if start to end is 90deg', () => {
    expect(describeArc(0, 0, 1, 0, 90)).to.equal('M 1 0 A 1 1 0 0 0 0 -1');
  });

  it('should match result if start to end is 180deg', () => {
    expect(describeArc(0, 0, 1, 0, 180)).to.equal('M 0 1 A 1 1 0 0 0 0 -1');
  });

  it('should match result if start to end is 270deg', () => {
    expect(describeArc(0, 0, 1, 0, 270)).to.equal('M -1 0 A 1 1 0 1 0 0 -1');
  });

  it('should match result if start to end is 360deg', () => {
    expect(describeArc(0, 0, 1, 0, 360)).to.equal('M 0 -1 A 1 1 0 1 0 0 -1');
  });

  it('should have limits of 0 to 360 for start and end angles', () => {
    // same as 0, 0)
    expect(describeArc(0, 0, 1, -10, -10)).to.equal('M 0 -1 A 1 1 0 0 0 0 -1');
    // same as 0, 0)
    expect(describeArc(0, 0, 1, 370, 370)).to.equal('M 0 -1 A 1 1 0 0 0 0 -1');
  });
});
