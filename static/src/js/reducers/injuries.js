import ActionTypes from '../action-types.js';
import merge from 'lodash/merge';

const initialState = {};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_INJURIES_SUCCESS:
      return merge({}, state, action.body.injuries);


    default:
      return state;
  }
};
