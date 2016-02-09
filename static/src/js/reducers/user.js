import ActionTypes from '../action-types';


const initialState = {
  user: {},
  infoFormErrors: {},
  addressFormErrors: {},
};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_USER_SUCCESS:
      return Object.assign({}, state, {
        user: action.body,
      });

    case ActionTypes.UPDATE_USER_INFO_SUCCESS:
      // TODO: update user with the response
      return Object.assign({}, state, {
        infoFormErrors: {},
      });

    case ActionTypes.UPDATE_USER_ADDRESS_SUCCESS:
      // TODO: update user with the response
      return Object.assign({}, state, {
        addressFormErrors: {},
      });

    case ActionTypes.UPDATE_USER_INFO_FAIL:
      return Object.assign({}, state, {
        infoFormErrors: action.ex.response.body.errors,
      });

    case ActionTypes.UPDATE_USER_ADDRESS_FAIL:
      return Object.assign({}, state, {
        addressFormErrors: action.ex.response.body.errors,
      });

    default:
      return state;
  }
};
