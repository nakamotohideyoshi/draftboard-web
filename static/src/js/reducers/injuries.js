import ActionTypes from '../action-types.js';
import { merge as _merge } from 'lodash';

const initialState = {};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_INJURIES_SUCCESS:
      return _merge({}, state, action.body.injuries);


    default:
      return state;
  }
};
