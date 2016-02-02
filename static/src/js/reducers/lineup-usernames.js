import update from 'react-addons-update';
import _ from 'lodash';
import * as ActionTypes from '../action-types';


module.exports = (state = {}, action) => {
  switch (action.type) {
    case ActionTypes.REQUEST_LINEUP_USERNAMES:
      return update(state, {
        [action.contestId]: {
          $set: {
            isFetching: true,
            lineups: [],
          },
        },
      });

    case ActionTypes.RECEIVE_LINEUP_USERNAMES:
      return update(state, {
        [action.contestId]: {
          $set: {
            isFetching: true,
            lineups: action.lineups,
          },
        },
      });

    default:
      return state;
  }
};
