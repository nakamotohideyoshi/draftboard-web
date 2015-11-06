import * as types from '../action-types.js';
let request = require('superagent');


function determineDraftability(player) {
  return true;
}





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



export function fetchDraftGroup(draftGroupId) {
  return (dispatch) => {
    return request
      .get("/draft-group/" + draftGroupId + '/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          return dispatch(fetchDraftgroupFail(err));
        } else {
          return dispatch(fetchDraftgroupSuccess(res.body));
        }
      });
  };
}
