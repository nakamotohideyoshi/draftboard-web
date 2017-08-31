import { createSelector } from 'reselect';

const historySelector = (state) => state.events.history;

/**
 * Returns an array of event items in the history.
 */
export const pastEvents = createSelector([historySelector], (history) => (
  history.map((value, index) => history[index])
));

/**
 * Returns an event matching the specified `eventId` from the provided history.
 * @param  {array}  history  An array of event history items.
 * @param  {string} eventId  The event's ID.
 * @return {object}          An event matching the provided `eventId` or `null`.
 */
export const selectEventFromHistory = (history, eventId) => {
  const matches = history.filter(event => event.id === eventId);
  return matches.length ? matches[0] : null;
};

/**
 * Returns true if the event was previously found in the history.
 * @param  {array}  history  An array of event history items.
 * @param  {string}  eventId [description]
 * @return {Boolean}         [description]
 */
export const isPastEvent = (history, eventId) => (
  selectEventFromHistory(history, eventId) !== null
);
