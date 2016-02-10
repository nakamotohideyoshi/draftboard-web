import update from 'react-addons-update';
import ActionTypes from '../action-types';


const defaultState = {
  stats: {
    winnings: '-',
    possible: '-',
    fees: '-',
    entries: 0,
    contests: 0,
  },
  lineups: [],
};

module.exports = (state = defaultState, action) => {
  switch (action.type) {
    case ActionTypes.REQUEST_LINEUPS_RESULTS:
      return update(state, {
        $set: {
          isFetching: true,
        },
      });

    case ActionTypes.RECEIVE_LINEUPS_RESULTS:
      return update(state, {
        $set: {
          stats: action.stats,
          lineups: action.lineups,
          isFetching: false,
        },
      });

    default:
      return state;
  }
};
