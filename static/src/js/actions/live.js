import * as ActionTypes from '../action-types'
import _ from 'lodash'

import { fetchContestLineupsUsernamesIfNeeded } from './live-contests'
import { fetchPlayersStatsIfNeeded } from './live-players'

export function updateLiveMode(newMode) {
  return (dispatch, getState) => {
    const state = getState()

    // check that we have relevant players
    if (newMode.myLineupId && state.livePlayers.fetched.indexOf(newMode.myLineupId) === -1) {
      dispatch(fetchPlayersStatsIfNeeded(newMode.myLineupId))
    }
    if (newMode.opponentLineupId && state.livePlayers.fetched.indexOf(newMode.opponentLineupId) === -1) {
      dispatch(fetchPlayersStatsIfNeeded(newMode.opponentLineupId))
    }

    // make sure to get the usernames as well
    if (newMode.contestId) {
      dispatch(fetchContestLineupsUsernamesIfNeeded(newMode.contestId))
    }


    // make sure every defined field is an integer
    _.forEach(newMode, (val, key) => {
      newMode[key] = val === undefined ? undefined : parseInt(val)
    })

    return dispatch({
        type: ActionTypes.LIVE_MODE_CHANGED,
        mode: newMode
      }
    )
  }
}
