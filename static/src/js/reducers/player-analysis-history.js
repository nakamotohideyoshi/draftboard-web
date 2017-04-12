import * as ActionTypes from '../action-types.js';
import mergeWith from 'lodash/mergeWith';
import isArray from 'lodash/isArray';

const initialState = {
  playerAnalysisAndHistory: [],
};

module.exports = (state = initialState, action = {}) => {
  switch (action.type) {

    case ActionTypes.PLAYER_NEWS_SINGLE__RECEIVE:
      {
        const { fields } = action.response;
        // result.playerAnalysisAndHistory = fields;
        return mergeWith({}, state, { playerAnalysisAndHistory: fields }, (objValue, srcValue) => {
          if (isArray(srcValue)) {
            return srcValue;
          }
        });
      }

    default:
      return state;
  }
};
