import * as ActionTypes from '../action-types'


export function updateLiveMode(type, id) {
  return {
    type: ActionTypes.LIVE_MODE_CHANGED,
    mode: {
      type,
      id
    }
  }
}
