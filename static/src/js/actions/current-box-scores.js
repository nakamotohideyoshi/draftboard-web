"use strict"

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import _ from 'lodash'


export function mergeBoxScores(boxScores) {
  log.debug('actionsCurrentBoxScores.mergeBoxScores')

  _.forEach(boxScores, (boxScore) => {
    const fields = boxScore.fields
    boxScore.teams = {}

    boxScore.teams[fields.srid_home] = {
      score: fields.home_score,
      name: fields.home_abbr
    }

    boxScore.teams[fields.srid_away] = {
      score: fields.away_score,
      name: fields.away_abbr
    }
  })

  return {
    type: ActionTypes.MERGE_CURRENT_BOX_SCORES,
    boxScores: boxScores
  }
}


export function updateBoxScore(id, event) {
  log.debug('actionsCurrentBoxScores.updateBoxScore')

  return (dispatch, getState) => {
    const state = getState()
    const updatedScore = state.currentBoxScores[id].teams[event.team].score + event.points

    return dispatch({
        type: ActionTypes.UPDATE_CURRENT_BOX_SCORE,
        id: id,
        team: event.team,
        score: updatedScore
    })
  }
}
