'use strict';

import { expect } from 'chai';
import {
  getDaysForMonth,
  daysToWeekView,
  weekdayNumToName
} from '../../lib/time.js';

describe('Time', function() {

  describe('weekdayNumToName', function () {
    it('should return the name of the weekday for its number, starting from 0', function() {
      expect(weekdayNumToName(0)).to.equal('MON');
      expect(weekdayNumToName(1)).to.equal('TUE');
      expect(weekdayNumToName(2)).to.equal('WED');
      expect(weekdayNumToName(3)).to.equal('THU');
      expect(weekdayNumToName(4)).to.equal('FRI');
      expect(weekdayNumToName(5)).to.equal('SAT');
      expect(weekdayNumToName(6)).to.equal('SUN');
    });
  });

  describe('getDaysForMonth', function () {
    it('should return a list of Date objects for provided year and month', function() {
      expect(getDaysForMonth(2015, 1).toString()).to.equal([
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
      ].toString());

      expect(getDaysForMonth(2016, 0).toString()).to.equal([
        new Date(2016, 0, 1),
        new Date(2016, 0, 2),
        new Date(2016, 0, 3),
        new Date(2016, 0, 4),
        new Date(2016, 0, 5),
        new Date(2016, 0, 6),
        new Date(2016, 0, 7),
        new Date(2016, 0, 8),
        new Date(2016, 0, 9),
        new Date(2016, 0, 10),
        new Date(2016, 0, 11),
        new Date(2016, 0, 12),
        new Date(2016, 0, 13),
        new Date(2016, 0, 14),
        new Date(2016, 0, 15),
        new Date(2016, 0, 16),
        new Date(2016, 0, 17),
        new Date(2016, 0, 18),
        new Date(2016, 0, 19),
        new Date(2016, 0, 20),
        new Date(2016, 0, 21),
        new Date(2016, 0, 22),
        new Date(2016, 0, 23),
        new Date(2016, 0, 24),
        new Date(2016, 0, 25),
        new Date(2016, 0, 26),
        new Date(2016, 0, 27),
        new Date(2016, 0, 28),
        new Date(2016, 0, 29),
        new Date(2016, 0, 30),
        new Date(2016, 0, 31)
      ].toString());
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
