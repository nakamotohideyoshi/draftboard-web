import 'babel-core/polyfill';
import * as types from '../action-types.js'
import request from 'superagent'



function fetchingFeaturedContests() {
  return {
    type: types.FETCHING_FEATURED_CONTESTS
  };
}


function fetchFeaturedContestsSuccess(body) {
  return {
    type: types.FETCH_FEATURED_CONTESTS_SUCCESS,
    contests: body
  };
}


function fetchFeaturedContestsFail(ex) {
  console.error(ex)
  return {
    type: types.FETCH_FEATURED_CONTESTS_FAIL,
    ex
  };
}


// Do we need to fetch the featured contests?
function shouldFetchFeaturedContests(state) {
  const features = state.featuredContests

  if (!features.banners.length) {
    // if there aren't any in the store, we probably need to fetch them.
    return true
  } else if (features.isFetching) {
    // are we currently fetching it?
    return false
  } else {
    // Default to true.
    return true
  }
}



export function fetchFeaturedContestsIfNeeded() {
  return (dispatch, getState) => {
    if(shouldFetchFeaturedContests(getState())) {
      return dispatch(fetchFeaturedContests())
    } else {
      return Promise.resolve()
    }
  };
}



export function fetchFeaturedContests() {
  return (dispatch) => {
    dispatch(fetchingFeaturedContests)

    return new Promise((resolve, reject) => {
      request
      .get("/api/lobby/featured-content/")
      .set({
        'X-REQUESTED-WITH': 'XMLHttpRequest',
        'Accept': 'application/json'
      })
      .end(function(err, res) {
        if(err) {
          dispatch(fetchFeaturedContestsFail(err))
          reject(err)
        } else {
          dispatch(fetchFeaturedContestsSuccess(res.body))
          resolve(res)
        }
      })
    })
  }
}
