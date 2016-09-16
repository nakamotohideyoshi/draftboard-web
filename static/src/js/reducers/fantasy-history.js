import ActionTypes from '../action-types.js';
import merge from 'lodash/merge';

const initialState = {};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FANTASY_HISTORY__FETCH_SUCCESS:
      return merge({}, state, action.response);

    default:
      return state;
  }
};
