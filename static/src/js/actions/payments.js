import * as types from '../action-types';
import request from 'superagent';
import Cookies from 'js-cookie';


function fetchPaymentMethodsSuccess(body) {
  return {
    type: types.FETCH_PAYMENT_METHODS_SUCCESS,
    body,
  };
}


function fetchPaymentMethodsFail(ex) {
  return {
    type: types.FETCH_PAYMENT_METHODS_FAIL,
    ex,
  };
}

export function fetchPaymentMethods() {
  return (dispatch) => request
    .get('/api/account/paypal/saved-card/list/')
    .set({ 'X-REQUESTED-WITH': 'XMLHttpRequest' })
    .set('Accept', 'application/json')
    .end((err, res) => {
      if (err) {
        return dispatch(fetchPaymentMethodsFail(err));
      }

      return dispatch(fetchPaymentMethodsSuccess(res.body));
    });
}


function addPaymentMethodSuccess(body) {
  return {
    type: types.ADD_PAYMENT_METHOD_SUCCESS,
    body,
  };
}


function addPaymentMethodFail(ex) {
  return {
    type: types.ADD_PAYMENT_METHOD_FAIL,
    ex,
  };
}


export function addPaymentMethod(postData) {
  return (dispatch) => request
    .post('/api/account/paypal/saved-card/add/')
    .send(postData)
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .end((err, res) => {
      if (err) {
        return dispatch(addPaymentMethodFail(err));
      }
      return dispatch(addPaymentMethodSuccess(res.body));
    });
}


function setPaymentMethodDefaultSuccess(id) {
  return {
    type: types.SET_PAYMENT_METHOD_DEFAULT_SUCCESS,
    id,
  };
}


function setPaymentMethodDefaultFail(ex) {
  return {
    type: types.SET_PAYMENT_METHOD_DEFAULT_FAIL,
    ex,
  };
}


export function setPaymentMethodDefault(id) {
  return (dispatch) => request
    .post('/account/api/account/payments/setdefault/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .end((err) => {
      if (err) {
        return dispatch(setPaymentMethodDefaultFail(err));
      }

      return dispatch(setPaymentMethodDefaultSuccess(id));
    });
}


function removePaymentMethodSuccess(id) {
  return {
    type: types.REMOVE_PAYMENT_METHOD_SUCCESS,
    id,
  };
}


function removePaymentMethodFail(ex) {
  return {
    type: types.REMOVE_PAYMENT_METHOD_FAIL,
    ex,
  };
}


export function removePaymentMethod(id) {
  return (dispatch) => request
    .del('/account/api/account/payments/remove/1/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .end((err) => {
      if (err) {
        return dispatch(removePaymentMethodFail(err));
      }

      return dispatch(removePaymentMethodSuccess(id));
    });
}


function withdrawSuccess(body) {
  return {
    type: types.WITHDRAW_AMOUNT_SUCCESS,
    body,
  };
}


function withdrawFail(ex) {
  return {
    type: types.WITHDRAW_AMOUNT_FAIL,
    ex,
  };
}


export function withdraw(postData) {
  return (dispatch) => request
    .post('/account/api/account/payments/withdraw/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .send(postData)
    .end((err, res) => {
      if (err) {
        return dispatch(withdrawFail(err));
      }

      return dispatch(withdrawSuccess(res.body));
    });
}


function depositSuccess(body) {
  return {
    type: types.DEPOSIT_SUCCESS,
    body,
  };
}


function depositFail(ex) {
  return {
    type: types.DEPOSIT_FAIL,
    ex,
  };
}


export function deposit() {
  return (dispatch) => request
    .post('/account/api/account/payments/deposit/')
    .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
    .send({})
    .end((err, res) => {
      if (err) {
        return dispatch(depositFail(err));
      }
      return dispatch(depositSuccess(res.body));
    });
}
