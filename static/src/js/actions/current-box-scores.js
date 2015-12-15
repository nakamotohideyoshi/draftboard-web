"use strict"

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import _ from 'lodash'


export function mergeBoxScores(boxScores) {
  log.debug('actionsCurrentBoxScores.mergeBoxScores')

  let scoresBySRID = {}

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

    scoresBySRID[fields.srid_game] = boxScore
  })

  return {
    type: ActionTypes.MERGE_CURRENT_BOX_SCORES,
    boxScores: scoresBySRID
  }
}


export function updateBoxScore(gameId, teamId, points) {
  log.debug('actionsCurrentBoxScores.updateBoxScore')

  return {
    type: ActionTypes.UPDATE_CURRENT_BOX_SCORE,
    id: gameId,
    team: teamId,
    score: points
  }
}
