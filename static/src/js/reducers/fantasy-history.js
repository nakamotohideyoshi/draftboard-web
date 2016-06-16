import ActionTypes from '../action-types.js';
import merge from 'lodash/merge';

const initialState = {};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_FANTASY_HISTORY_SUCCESS:
      return merge({}, state, action.body.history);


    default:
      return state;
  }
};
