import * as ActionTypes from '../action-types';


/**
 * Takes a object of lineup objects and adds them to the store. Method is run with dispatch() to tie to the reducer
 * with according action type.
 * @param  {object} lineups List of lineup objects
 * @return {object}         Need data for the reducer
 */
export const setCurrentLineups = (lineups) => ({
  type: ActionTypes.SET_CURRENT_LINEUPS,
  lineups,
  updatedAt: Date.now(),
});
