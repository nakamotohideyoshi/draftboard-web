import * as types from '../action-types.js';
import merge from 'lodash/merge';


const initialState = {
  isFetching: false,
  banners: [],
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case types.FETCHING_FEATURED_CONTESTS:
      return merge({}, state, {
        isFetching: true,
      });


    case types.FETCH_FEATURED_CONTESTS_FAIL:
      return merge({}, state, {
        isFetching: false,
      });


    case types.FETCH_FEATURED_CONTESTS_SUCCESS:
      return merge({}, state, {
        isFetching: false,
        banners: action.contests,
      });


    default:
      return state;
  }
};
