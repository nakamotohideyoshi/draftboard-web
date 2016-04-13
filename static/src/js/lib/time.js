import log from './logging.js';


/**
 * This module contains some time related utility functions.
 */

/**
 * Returns a list of Date objects. Each object represents a day
 * from the provided month.
 * @return {Array}
 */
export function getDaysForMonth(year, month) {
  const date = new Date(year, month, 1);
  const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);

  return (Array.apply(null, Array(lastDay.getDate()))).map((_, i) => {
    return new Date(date.getFullYear(), date.getMonth(), i + 1);
  });
}

/**
 * Returns a list of Date objects. Each object represents a day
 * from the current month.
 * @return {Array}
 */
export function getDaysForThisMonth() {
  const date = new Date();
  return getDaysForMonth(date.getFullYear(), date.getMonth());
}

/**
 * Returns weekday name from it's number from `Date.prototype.getDay()`.
 * @param {Number} dayNum
 * @return {String}
 */
export function weekdayNumToName(dayNum) {
  switch (dayNum) {
    case 0: return 'SUN';
    case 1: return 'MON';
    case 2: return 'TUE';
    case 3: return 'WED';
    case 4: return 'THU';
    case 5: return 'FRI';
    case 6: return 'SAT';
    default:
      throw new Error(`Unknown weekday number: ${dayNum}`);
  }
}

/**
 * Returns month name from it's number from `Date.prototype.getMonth()`.
 * @param {Number} monthNum
 * @return {String}
 */
export function monthNumToName(monthNum) {
  switch (monthNum) {
    case 0: return 'January';
    case 1: return 'February';
    case 2: return 'March';
    case 3: return 'April';
    case 4: return 'May';
    case 5: return 'June';
    case 6: return 'July';
    case 7: return 'August';
    case 8: return 'September';
    case 9: return 'October';
    case 10: return 'November';
    case 11: return 'December';
    default:
      throw new Error(`Unknown month number: ${monthNum}`);
  }
}

/**
 * Returns month name from it's number from `Date.prototype.getMonth()`.
 * @param {Array} days List containing the days of the month as Date objects.
 * @return {Array} Matrix representing weeks of the month.
 */
export function daysToWeekView(days) {
  let prevMonth = getDaysForMonth(days[0].getFullYear(), days[0].getMonth() - 1);
  let nextMonth = getDaysForMonth(days[0].getFullYear(), days[0].getMonth() + 1);

  // Handle first week separately as it can be incomplete.
  let firstWeek = [];
  let firstWeekLength = 0;

  if (days[0].getDay() !== 1) {
    for (let i = -1; days[++i].getDay() !== 1;) {
      firstWeek.push(days[i]);
    }

    firstWeekLength = firstWeek.length;
    while (firstWeek.length != 7) firstWeek.unshift(prevMonth.pop());
  }

  let groupedByWeekDay = days.slice(firstWeekLength).reduce((accum, d) => {
    accum[d.getDay()] = accum[d.getDay()] || [];
    accum[d.getDay()].push(d);

    return accum;
  }, []);

  // Make Sunday the last day, not the first.
  groupedByWeekDay.push(groupedByWeekDay.shift());

  // Transpose `groupedByDay` to get array of days per weeks. If
  // last week is incomplete this row may add some undefined days.
  let daysPerWeeks = groupedByWeekDay[0].map((coll, i) => {
    return groupedByWeekDay.map((row) => {
      return row[i];
    });
  });

  // Fill last week if it is incomplete.
  let lastWeek = daysPerWeeks[daysPerWeeks.length - 1];
  while (lastWeek[lastWeek.length - 1] == null) lastWeek.pop();
  while (lastWeek.length != 7) lastWeek.push(nextMonth.shift());

  let result = daysPerWeeks;
  if (firstWeekLength > 0) {
    result = [firstWeek].concat(result);
  }

  return result;
}


/**
 * Returns date in string format with the selected delimiter
 * MM [-] DD [-] YYYY
 */
export function stringifyDate(date, delimiter) {
  if (date && delimiter) {
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    return month + delimiter + day + delimiter + year;
  }

  log.warn('Missing date or delimiter parameter');
  return;
}
