import { createSelector } from 'reselect';


// All the live multipart events from socket connections
const allEventsMultipart = (state) => state.eventsMultipart;

// Filter by sport
export const eventsMultipart = createSelector(
  [allEventsMultipart],
  (events) => events.events
);
