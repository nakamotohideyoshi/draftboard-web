import * as types from '../action-types.js';
import { merge as _merge } from 'lodash';


const initialState = {
  isFetching: false,
  banners: [],
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case types.FETCHING_FEATURED_CONTESTS:
      return _merge({}, state, {
        isFetching: true,
      });


    case types.FETCH_FEATURED_CONTESTS_FAIL:
      return _merge({}, state, {
        isFetching: false,
      });


    case types.FETCH_FEATURED_CONTESTS_SUCCESS:
      return _merge({}, state, {
        isFetching: false,
        banners: action.contests,
      });


    default:
      return state;
  }
};
