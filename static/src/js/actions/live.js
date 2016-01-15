import * as ActionTypes from '../action-types'

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

    return dispatch({
        type: ActionTypes.LIVE_MODE_CHANGED,
        mode: newMode
      }
    )
  }
}
