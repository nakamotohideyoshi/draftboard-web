import ActionTypes from '../action-types.js';
import { merge as _merge } from 'lodash';

const initialState = {};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_FANTASY_HISTORY_SUCCESS:
      return _merge({}, state, action.body.history);


    default:
      return state;
  }
};
