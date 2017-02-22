import log from './logging.js';


/**
 * This module contains some time related utility functions.
 */

/**
 * Returns a list of Date objects. Each object represents a day
 * from the provided month. Months are zero based.
 * @return {Array}
 */
export function getDaysForMonth(year, month) {
  const date = new Date(year, month - 1, 1);
  const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);

  return (Array.apply(null, Array(lastDay.getDate()))).map((_, i) => {
    return new Date(date.getFullYear(), date.getMonth(), i + 1);
  });
}

/**
 * Returns weekday name from it's number from `Date.prototype.getDay()`.
 * @param {Number} dayNum
 * @return {String}
 */
export function weekdayNumToName(dayNum) {
  switch (dayNum) {
    case 0: return 'MON';
    case 1: return 'TUE';
    case 2: return 'WED';
    case 3: return 'THU';
    case 4: return 'FRI';
    case 5: return 'SAT';
    case 6: return 'SUN';
    default:
      throw new Error(`Unknown weekday number: ${dayNum}`);
  }
}

/**
 * Returns month name from it's number based on 1-12.
 * @param {Number} monthNum
 * @return {String}
 */
export function monthNumToName(monthNum) {
  switch (monthNum) {
    case 1: return 'January';
    case 2: return 'February';
    case 3: return 'March';
    case 4: return 'April';
    case 5: return 'May';
    case 6: return 'June';
    case 7: return 'July';
    case 8: return 'August';
    case 9: return 'September';
    case 10: return 'October';
    case 11: return 'November';
    case 12: return 'December';
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
  const initialMonth = days[0].getMonth() + 1;
  let prevMonth = getDaysForMonth(days[0].getFullYear(), initialMonth - 1);
  let nextMonth = getDaysForMonth(days[0].getFullYear(), initialMonth + 1);

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
    // const day = date.getDate();
    // const month = date.getMonth() + 1;
    // const year = date.getFullYear();
    // return month + delimiter + day + delimiter + year;
    console.log(date)
    return date.format('MM'+ delimiter +'DD'+ delimiter + 'YYYY')
  }

  log.warn('Missing date or delimiter parameter');
  return;
}
