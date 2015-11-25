import * as moment from 'moment'


/**
 * Adds a leading 0 to turn single-digit numbers into 2-digit ones. Used for displaying time.
 * @param {Integer} number
 */
export function toTwoDigit(number) {
  return (Math.abs(number) < 10) ? "0" + Math.abs(number) : Math.abs(number)
}


/**
 * From a UTC timestamp, determine the time remaining, parsed out into hours, minutes, and seconds.
 * @param  {[type]} timestamp A UTC timestamp.
 * @return {Object}           Hours, Minutes and Seconds remaining until the timestamp.
 */
export function timeRemaining(timestamp) {
  // difference between when the contest starts and now (in ms).
  let diffTime = moment.utc(timestamp) - moment.utc()
  // convert to a moment 'duration' so we can parse it out.
  let duration = moment.duration(diffTime)

  return {
    hours: Math.floor(duration.asHours()),
    minutes: toTwoDigit(duration.minutes()),
    seconds: toTwoDigit(duration.seconds())
  }
}
