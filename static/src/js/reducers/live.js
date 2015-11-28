import update from 'react-addons-update'

import * as ActionTypes from '../action-types'
import { forEach as _forEach } from 'lodash'
import log from '../lib/logging'


// Reducer for the live section, stores what mode the app is in
module.exports = function(state = {
  mode: {
    // TODO live - make this dynamic based on lineup/contest
    type: 'lineup',
    draftGroupId: 1,
    lineupId: 1,
    contestId: null
  }
}, action) {
  switch (action.type) {
    case ActionTypes.LIVE_MODE_CHANGED:
      log.debug('reducersLive.LIVE_MODE_CHANGED')

      return update(state, { mode: {
        $set: action.mode
      }})

    default:
      return state
  }
};
