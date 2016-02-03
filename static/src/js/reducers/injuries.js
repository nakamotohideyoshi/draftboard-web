import ActionTypes from '../action-types.js';

const initialState = {};


module.exports = (state = initialState, action) => {
  switch (action.type) {

    case ActionTypes.FETCH_INJURIES_SUCCESS:
      return Object.assign({}, state, action.body.injuries);


    default:
      return state;
  }
};
