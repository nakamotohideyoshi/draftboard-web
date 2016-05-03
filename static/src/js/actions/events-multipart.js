import * as ActionTypes from '../action-types';
import store from '../store';


// dispatch to reducer methods

const addEventMultipart = (key, value) => ({
  type: ActionTypes.EVENT_MULTIPART_ADD,
  key,
  value,
});

const updateEventMultipart = (key, value) => ({
  type: ActionTypes.EVENT_MULTIPART_UPDATE,
  key,
  value,
});

export const removeMultipartEvent = (key) => ({
  type: ActionTypes.EVENT_MULTIPART_REMOVE,
  key,
});


// primary methods (mainly exported, some needed in there to have proper init of const)


/**
 * Store a multipart event, by either adding new or updating existing
 * @param  {string} key       Unique ID. Correlates to at_bat__id for mlb, drive__id for nfl
 * @param  {object} value     All relevant data related to event
 * NOTE: this method must be wrapped with dispatch()
 * @return {object}   Changes for reducer
 */
export const storeEventMultipart = (key, value) => {
  const state = store.getState();

  if (state.eventsMultipart.events.hasOwnProperty(key)) {
    return store.dispatch(updateEventMultipart(key, value));
  }

  return store.dispatch(addEventMultipart(key, value));
};
