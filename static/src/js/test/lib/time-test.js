'use strict';

import {expect} from 'chai';
import {getDaysForMonth, daysToWeekView} from '../../lib/time.js';

describe('Time', function() {

  describe('getDaysForMonth', function () {
    it('should return a list of Date objects for provided year and month', function() {
      const result = [
        new Date(2015, 1, 1),
        new Date(2015, 1, 2),
        new Date(2015, 1, 3),
        new Date(2015, 1, 4),
        new Date(2015, 1, 5),
        new Date(2015, 1, 6),
        new Date(2015, 1, 7),
        new Date(2015, 1, 8),
        new Date(2015, 1, 9),
        new Date(2015, 1, 10),
        new Date(2015, 1, 11),
        new Date(2015, 1, 12),
        new Date(2015, 1, 13),
        new Date(2015, 1, 14),
        new Date(2015, 1, 15),
        new Date(2015, 1, 16),
        new Date(2015, 1, 17),
        new Date(2015, 1, 18),
        new Date(2015, 1, 19),
        new Date(2015, 1, 20),
        new Date(2015, 1, 21),
        new Date(2015, 1, 22),
        new Date(2015, 1, 23),
        new Date(2015, 1, 24),
        new Date(2015, 1, 25),
        new Date(2015, 1, 26),
        new Date(2015, 1, 27),
        new Date(2015, 1, 28)
      ].toString();
      expect(getDaysForMonth(2015, 1).toString()).to.equal(result);
    });
  });

  describe('daysToWeekView', function () {
    it('should return a list of Date objects for provided year and month',
       function() {
         const result = [
           [new Date(2014, 1, -4),
            new Date(2014, 1, -3),
            new Date(2014, 1, -2),
            new Date(2014, 1, -1),
            new Date(2014, 1, 0),
            new Date(2014, 1, 1),
            new Date(2014, 1, 2)],
           [
             new Date(2014, 1, 3),
             new Date(2014, 1, 4),
             new Date(2014, 1, 5),
             new Date(2014, 1, 6),
             new Date(2014, 1, 7),
             new Date(2014, 1, 8),
             new Date(2014, 1, 9),
           ],
           [
             new Date(2014, 1, 10),
             new Date(2014, 1, 11),
             new Date(2014, 1, 12),
             new Date(2014, 1, 13),
             new Date(2014, 1, 14),
             new Date(2014, 1, 15),
             new Date(2014, 1, 16),
           ],
           [
             new Date(2014, 1, 17),
             new Date(2014, 1, 18),
             new Date(2014, 1, 19),
             new Date(2014, 1, 20),
             new Date(2014, 1, 21),
             new Date(2014, 1, 22),
             new Date(2014, 1, 23)
           ],
           [
             new Date(2014, 1, 24),
             new Date(2014, 1, 25),
             new Date(2014, 1, 26),
             new Date(2014, 1, 27),
             new Date(2014, 1, 28),
             new Date(2014, 2, 1),
             new Date(2014, 2, 2)
           ]
         ].toString();
         expect(daysToWeekView(getDaysForMonth(2014, 1)).toString()).to.equal(result);
    });
  });

});
