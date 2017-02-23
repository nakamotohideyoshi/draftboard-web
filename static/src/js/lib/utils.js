import moment from 'moment';


/**
 * Adjust datetime by the delta provided by Django. On production the delta is 0.
 * @return {object} Moment.js object
 */
export const dateNow = () => new Date().getTime() - (window.dfs.replayerTimeDelta * 1000);

/**
 * Checks if provided date is in the future.
 * @return {Number} timestamp
 */
export const isDateInTheFuture = (timestamp) => timestamp > dateNow();

/**
 * Adds a leading 0 to turn single-digit numbers into 2-digit ones. Used for displaying time.
 * @param {Integer} number
 */
export function toTwoDigit(number) {
  // Don't add a leading zero to negative numbers.
  if (number < 0) {
    return number;
  }

  return (number < 10) ? `0${number}` : number;
}


/**
 * From a UTC timestamp, determine the time remaining, parsed out into hours, minutes, and seconds.
 * @param  {[type]} timestamp A UTC timestamp.
 * @return {Object} Hours, Minutes and Seconds remaining until the timestamp.
 */
export function timeRemaining(timestamp) {
  const diffTime = moment.utc(timestamp) - moment(dateNow()).utc();
  // convert to a moment 'duration' so we can parse it out.
  const duration = moment.duration(diffTime);

  // if the time has expired, then return all zeros
  if (diffTime < 0) {
    return {
      expired: true,
      hours: '00',
      minutes: '00',
      seconds: '00',
    };
  }

  // The hours have no Math.abs because should be displayed as negative. (-32:05:57)
  // A negative number means that the thing we're counting down to has past.
  return {
    expired: false,
    hours: toTwoDigit(Math.floor(duration.asHours())),
    minutes: toTwoDigit(Math.abs(duration.minutes())),
    seconds: toTwoDigit(Math.abs(duration.seconds())),
  };
}

/**
 * Super shortcut so we always remember expiration is greater than now
 * @param  {mixed} expiresAt  Can have any date format
 * @return {boolean}          True if expired, false if not
 */
export const hasExpired = (expiresAt) => {
  if (typeof expiresAt === 'number') return dateNow() > expiresAt;

  return dateNow() > new Date(expiresAt).getTime();
};

// Has this timestamp passed?
export function isTimeInFuture(timestamp) {
  return moment.utc(timestamp) > moment(dateNow()).utc();
}

/**
 * Round a provided number to X decimal places
 */
export function roundUpToDecimalPlace(number, places) {
  return (Math.round(number * 10) / 10).toFixed(places);
}


/**
 * Remove a specific parameter from the url .search
 * @param  {[type]} sourceURL    [description]
 * @param  {[type]} key [description]
 * @return {[type]}               [description]
 */
export function removeParamFromURL(sourceURL, key) {
  let rtn = sourceURL.split('?')[0];
  let param;
  let paramsArr = [];
  const queryString = (sourceURL.indexOf('?') !== -1) ? sourceURL.split('?')[1] : '';

  if (queryString !== '') {
    paramsArr = queryString.split('&');
    for (let i = paramsArr.length - 1; i >= 0; i -= 1) {
      param = paramsArr[i].split('=')[0];
      if (param === key) {
        paramsArr.splice(i, 1);
      }
    }

    rtn = `${rtn}?${paramsArr.join('&')}`;
  }
  return rtn;
}


export function querystring() {
  // This function is anonymous, is executed immediately and
  // the return value is assigned to QueryString!
  const queryString = {};
  const query = window.location.search.substring(1);
  const vars = query.split('&');
  for (let i = 0; i < vars.length; i++) {
    const pair = vars[i].split('=');
        // If first entry with this name
    if (typeof queryString[pair[0]] === 'undefined') {
      queryString[pair[0]] = decodeURIComponent(pair[1]);
        // If second entry with this name
    } else if (typeof queryString[pair[0]] === 'string') {
      queryString[pair[0]] = [queryString[pair[0]], decodeURIComponent(pair[1])];
        // If third or later entry with this name
    } else {
      queryString[pair[0]].push(decodeURIComponent(pair[1]));
    }
  }
  return queryString;
}
