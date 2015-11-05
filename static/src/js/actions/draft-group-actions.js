import * as types from '../action-types.js';
let request = require('superagent');


function fetchDraftgroupSuccess(body) {
  return {
    type: types.FETCH_DRAFTGROUP_SUCCESS,
    body
  };
}


function fetchDraftgroupFail(ex) {
  return {
    type: types.FETCH_DRAFTGROUP_FAIL,
    ex
  };
}


export function fetchDraftgroup(draftGroupId) {
  console.log('fetchDraftgroup()', draftGroupId);

  return dispatch => {
    request
      .get("/draft-group/" + draftGroupId + '/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          dispatch(fetchDraftgroupFail(err));
        } else {
          dispatch(fetchDraftgroupSuccess(res.body));
        }
      });
  };
}
