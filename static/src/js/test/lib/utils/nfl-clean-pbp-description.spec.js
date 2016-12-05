import { expect } from 'chai';

import cleanDescription from '../../../lib/utils/nfl-clean-pbp-description';


describe('utils.numbers.cleanDescription', () => {
  it('should return proper sentences', () => {
    expect(cleanDescription(
      `
      (13:03) (Shotgun) 17-R.Tannehill pass short left to 14-J.Landry pushed ob at MIA 16 for -3 yards \
      (31-K.Chancellor). Penalty on MIA-10-K.Stills, Offensive Holding, declined.
      `
    )).to.equal(
      'R.Tannehill pass short left to J.Landry pushed out at MIA 16 for -3 yards.'
    );

    expect(cleanDescription(
      `
      (2:08) (Shotgun) 3-R.Wilson pass short left to 89-D.Baldwin ran ob at MIA 31 for 22 yards (24-I.Abdul-Quddus).
      `
    )).to.equal(
      'R.Wilson pass short left to D.Baldwin ran out at MIA 31 for 22 yards.'
    );

    expect(cleanDescription(
      `
      (9:23) 32-C.Michael right tackle to SEA 45 for 1 yard (50-A.Branch; 90-E.Mitchell). MIA-97-J.Phillips was
      injured during the play.
      `
    )).to.equal(
      'C.Michael right tackle to SEA 45 for 1 yard.'
    );

    expect(cleanDescription(
      `
      (2:06) (Shotgun) 17-R.Tannehill pass short middle to 84-J.Cameron to SEA 17 for 5 yards (54-B.Wagner)
      [56-C.Avril]. Official measurement.
      `
    )).to.equal(
      'R.Tannehill pass short middle to J.Cameron to SEA 17 for 5 yards[C.Avril].'
    );

    expect(cleanDescription(
      `
      (1:09) (Shotgun) 22-C.Prosise up the middle to SEA 15 for -2 yards (97-J.Phillips; 50-A.Branch).
      `
    )).to.equal(
      'C.Prosise up the middle to SEA 15 for -2 yards.'
    );
  });
});
