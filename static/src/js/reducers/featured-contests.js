import * as types from '../action-types.js';


const initialState = {
  isFetching: false,
  banners: [],
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case types.FETCHING_FEATURED_CONTESTS:
      return Object.assign({}, state, {
        isFetching: true,
      });


    case types.FETCH_FEATURED_CONTESTS_FAIL:
      return Object.assign({}, state, {
        isFetching: false,
      });


    case types.FETCH_FEATURED_CONTESTS_SUCCESS:
      return Object.assign({}, state, {
        isFetching: false,
        banners: action.contests,
      });


    default:
      return state;
  }
};
