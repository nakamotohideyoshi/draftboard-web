import * as moment from 'moment'


/**
 * Adds a leading 0 to turn single-digit numbers into 2-digit ones. Used for displaying time.
 * @param {Integer} number
 */
export function toTwoDigit(number) {
  // Don't add a leading zero to negative numbers.
  if (number < 0) {
    return number
  }

  return (number < 10) ? `0${number}` : number
}

/**
 * From a UTC timestamp, determine the time remaining, parsed out into hours, minutes, and seconds.
 * @param  {[type]} timestamp A UTC timestamp.
 * @return {Object} Hours, Minutes and Seconds remaining until the timestamp.
 */
export function timeRemaining(timestamp) {
  // difference between when the contest starts and now (in ms).
  const diffTime = moment.utc(timestamp) - moment.utc()
  // convert to a moment 'duration' so we can parse it out.
  const duration = moment.duration(diffTime)

  // if the time has expired, then return all zeros
  if (duration.seconds() <= 0) {
    return {
      expired: true,
      hours: '00',
      minutes: '00',
      seconds: '00',
    }
  }

  // The hours have no Math.abs because should be displayed as negative. (-32:05:57)
  // A negative number means that the thing we're counting down to has past.
  return {
    expired: false,
    hours: toTwoDigit(Math.floor(duration.asHours())),
    minutes: toTwoDigit(Math.abs(duration.minutes())),
    seconds: toTwoDigit(Math.abs(duration.seconds())),
  }
}

// Has this timestamp passed?
export function isTimeInFuture(timestamp) {
  return moment.utc(timestamp) > moment.utc()
}

/**
 * Round a provided number to X decimal places
 */
export function roundUpToDecimalPlace(number, places) {
  return (Math.round(number * 10) / 10).toFixed(places)
}
