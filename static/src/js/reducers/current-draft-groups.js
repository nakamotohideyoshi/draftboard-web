import update from 'react-addons-update';
import * as ActionTypes from '../action-types';


module.exports = (state = {
  items: [],
}, action) => {
  switch (action.type) {
    case ActionTypes.RECEIVE_CURRENT_DRAFT_GROUPS:
      return update(state, {
        $set: {
          isFetching: false,
          items: action.draftGroups,
          updatedAt: action.updatedAt,
        },
      });

    case ActionTypes.REQUEST_CURRENT_DRAFT_GROUPS:
      return update(state, {
        $set: {
          isFetching: true,
        },
      });

    default:
      return state;
  }
};
