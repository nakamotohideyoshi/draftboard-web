import * as ActionTypes from '../action-types'


export function updateLiveMode(newMode) {
  return {
    type: ActionTypes.LIVE_MODE_CHANGED,
    mode: newMode
  }
}
