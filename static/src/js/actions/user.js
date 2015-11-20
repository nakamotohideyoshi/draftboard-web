import * as types from '../action-types'
import request from 'superagent'
import Cookies from 'js-cookie'


function fetchUserSuccess(body) {
  return {
    type: types.FETCH_USER_SUCCESS,
    body
  };
}


function fetchUserFail(ex) {
  return {
    type: types.FETCH_USER_FAIL,
    ex
  };
}


export function fetchUser() {
  return (dispatch) => {
    return request
      .get('/account/api/account/user/')
      .set({'X-REQUESTED-WITH': 'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if (err) {
          return dispatch(fetchUserFail(err))
        } else {
          return dispatch(fetchUserSuccess(res.body))
        }
      });
  };
}


function updateUserInfoSuccess(body) {
  return {
    type: types.UPDATE_USER_INFO_SUCCESS,
    body
  };
}


function updateUserInfoFail(ex) {
  return {
    type: types.UPDATE_USER_INFO_FAIL,
    ex
  };
}


export function updateUserInfo(postData={}) {
  return (dispatch) => {
    return request
    .post('/account/api/account/user/')
    .set({'X-CSRFToken': Cookies.get('csrftoken')})
    .send(postData)
    .end(function(err, res) {
      if (err) {
        return dispatch(updateUserInfoFail(err))
      } else {
        return dispatch(updateUserInfoSuccess(res.body))
      }
    });
  };
}


function updateUserAddressSuccess(body) {
  return {
    type: types.UPDATE_USER_ADDRESS_SUCCESS,
    body
  };
}


function updateUserAddressFail(ex) {
  return {
    type: types.UPDATE_USER_ADDRESS_FAIL,
    ex
  };
}


export function updateUserAddress(postData={}) {
  return (dispatch) => {
    return request
      .post('/account/api/account/information/')
      .send(postData)
      .set({'X-CSRFToken': Cookies.get('csrftoken')})
      .end(function(err, res) {
        if (err) {
          return dispatch(updateUserAddressFail(err))
        } else {
          return dispatch(updateUserAddressSuccess(res.body))
        }
      });
  }
}
