import ActionTypes from '../action-types'


const initialState = {
  payments: [],
  depositFormErrors: {},
  withdrawalFormErrors: {}
}


module.exports = function(state = initialState, action) {

  switch(action.type) {

    case ActionTypes.FETCH_PAYMENTS_SUCCESS:
      return Object.assign({}, state, {
        payments: action.body
      });

    case ActionTypes.ADD_PAYMENT_METHOD_SUCCESS:
      return Object.assign({}, state, {
        payments: state.payments.append(action.body)
      });

    case ActionTypes.SET_PAYMENT_METHOD_DEFAULT_SUCCESS:
      return Object.assign({}, state, {
        payments: state.payments.map((payment) => {
          let toUpdate = payment;
          if (payment.id === action.id) {
            toUpdate.isDefault = true
          } else {
            toUpdate.isDefault = false
          }
          return toUpdate
        })
      });

    case ActionTypes.REMOVE_PAYMENT_METHOD_SUCCESS:
      return Object.assign({}, state, {
        payments: state.payments.filter((payment) => {return payment.id !== action.id})
      });

    case ActionTypes.DEPOSIT_SUCCESS:
      return Object.assign({}, state, {
        depositFormErrors: {}
      });

    case ActionTypes.DEPOSIT_FAIL:
      return Object.assign({}, state, {
        depositFormErrors: action.ex.response.body.errors
      });

    case ActionTypes.WITHDRAW_SUCCESS:
      return Object.assign({}, state, {
        withdrawalFormErrors: {}
      });

    case ActionTypes.WITHDRAW_FAIL:
      return Object.assign({}, state, {
        withdrawalFormErrors: action.ex.response.body.errors
      });

    default:
      return state;
  }
}
