import * as types from '../action-types'
import request from 'superagent'
import Cookies from 'js-cookie'


function fetchPaymentsSuccess(body) {
  return {
    type: types.FETCH_PAYMENTS_SUCCESS,
    body
  };
}


function fetchPaymentsFail(ex) {
  return {
    type: types.FETCH_PAYMENTS_FAIL,
    ex
  };
}

export function fetchPayments() {
  return (dispatch) => {
    return request
      .get('/account/api/account/payments/')
      .set({'X-REQUESTED-WITH': 'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if (err) {
          return dispatch(fetchPaymentsFail(err))
        } else {
          return dispatch(fetchPaymentsSuccess(res.body))
        }
      });
  };
}



function addPaymentMethodSuccess(body) {
  return {
    type: types.ADD_PAYMENT_METHOD_SUCCESS,
    body
  };
}


function addPaymentMethodFail(ex) {
  return {
    type: types.ADD_PAYMENT_METHOD_FAIL,
    ex
  };
}


export function addPaymentMethod(postData) {
  return (dispatch) => {
    return request
      .post('/account/api/account/payments/add/')
      .send(postData)
      .set({'X-CSRFToken': Cookies.get('csrftoken')})
      .end(function(err, res) {
        if (err) {
          return dispatch(addPaymentMethodFail(err))
        } else {
          return dispatch(addPaymentMethodSuccess(res.body))
        }
      });
  }
}


function setPaymentMethodDefaultSuccess(id) {
  return {
    type: types.SET_PAYMENT_METHOD_DEFAULT_SUCCESS,
    id
  };
}


function setPaymentMethodDefaultFail(ex) {
  return {
    type: types.SET_PAYMENT_METHOD_DEFAULT_FAIL,
    ex
  };
}


export function setPaymentMethodDefault(id) {
  return (dispatch) => {
    return request
      .post('/account/api/account/payments/setdefault/')
      .set({'X-CSRFToken': Cookies.get('csrftoken')})
      .end(function(err, res) {
        if (err) {
          return dispatch(setPaymentMethodDefaultFail(err))
        } else {
          return dispatch(setPaymentMethodDefaultSuccess(id))
        }
      })
  }
}


function removePaymentMethodSuccess(id) {
  return {
    type: types.REMOVE_PAYMENT_METHOD_SUCCESS,
    id
  };
}


function removePaymentMethodFail(ex) {
  return {
    type: types.REMOVE_PAYMENT_METHOD_FAIL,
    ex
  };
}


export function removePaymentMethod(id) {
  return (dispatch) => {
    return request
      .del('/account/api/account/payments/remove/1/')
      .set({'X-CSRFToken': Cookies.get('csrftoken')})
      .end(function(err, res) {
        if (err) {
          return dispatch(removePaymentMethodFail(err))
        } else {
          return dispatch(removePaymentMethodSuccess(id))
        }
      })
  }
}


function withdrawSuccess(body) {
  return {
    type: types.WITHDRAW_SUCCESS,
    body
  };
}


function withdrawFail(ex) {
  return {
    type: types.WITHDRAW_FAIL,
    ex
  };
}


export function withdraw(postData={}) {
  return (dispatch) => {
    return request
      .post('/account/api/account/payments/withdraw/')
      .set({'X-CSRFToken': Cookies.get('csrftoken')})
      .send({})
      .end(function(err, res) {
        if (err) {
          return dispatch(withdrawFail(err))
        } else {
          return dispatch(withdrawSuccess(res.body))
        }
      })
  }
}


function depositSuccess(body) {
  return {
    type: types.DEPOSIT_SUCCESS,
    body
  }
}


function depositFail(ex) {
  return {
    type: types.DEPOSIT_FAIL,
    ex
  }
}


export function deposit(postData={}) {
  return (dispatch) => {
    return request
      .post('/account/api/account/payments/deposit/')
      .set({'X-CSRFToken': Cookies.get('csrftoken')})
      .send({})
      .end(function(err, res) {
        if (err) {
          return dispatch(depositFail(err))
        } else {
          return dispatch(depositSuccess(res.body))
        }
      })
  }
}
