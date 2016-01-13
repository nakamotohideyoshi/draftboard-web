"use strict";

import update from 'react-addons-update'
const ActionTypes = require('../action-types');
import log from '../lib/logging'


module.exports = function(state = {
}, action) {
  switch (action.type) {
    case ActionTypes.MERGE_CURRENT_BOX_SCORES:
      log.trace('reducersCurrentBoxScores.MERGE_CURRENT_BOX_SCORES')
      return update(state, { $merge: action.boxScores })

    case ActionTypes.UPDATE_CURRENT_BOX_SCORE:
      log.debug('reducersCurrentBoxScores.UPDATE_CURRENT_BOX_SCORE')
      return update(state, {
        [action.id]: {
          teams: {
            [action.team]: {
              $set: {
                score: action.score
              }
            }
          }
        }
      })

    default:
      return state
  }
};
