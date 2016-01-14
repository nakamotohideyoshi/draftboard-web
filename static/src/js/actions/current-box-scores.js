"use strict"

import * as ActionTypes from '../action-types'
import log from '../lib/logging'
import _ from 'lodash'

export const GAME_DURATIONS = {
  nba: {
    periods: 4,
    periodMinutes: 12,
    gameMinutes: 48
  }
}

// TODO make this sport dependent
function calculateTimeRemaining(sport, game) {
  log.trace('actionsCurrentBoxScores.calculateTimeRemaining')
  const sportDurations = GAME_DURATIONS[sport]

  // if the game hasn't started, return full time
  if (!game.hasOwnProperty('boxscore')) {
    return sportDurations.gameMinutes
  }
  const boxScore = game.boxscore

  // if the game hasn't started but we have boxscore, return with full minutes
  if (boxScore.quarter === '') {
    return sportDurations.gameMinutes
  }

  const currentQuarter = boxScore.quarter
  const clockMinSec = boxScore.clock.split(':')

  // determine remaining minutes based on quarters
  const remainingQuarters = (currentQuarter > sportDurations.periods) ? 0 : sportDurations.periods - currentQuarter
  const remainingMinutes = remainingQuarters * 12

  // round up to the nearest minute
  return remainingMinutes + parseInt(clockMinSec[0]) + 1
}


export function mergeBoxScores(games) {
  log.trace('actionsCurrentBoxScores.mergeBoxScores')

  _.forEach(games, (game) => {
    if (game.hasOwnProperty('boxscore')) {
      let boxScore = game.boxscore
      boxScore.teamScores = {
        [boxScore.srid_home]: boxScore.home_score,
        [boxScore.srid_away]: boxScore.away_score
      }

      boxScore.timeRemaining = calculateTimeRemaining('nba', game)
    }
  })

  return {
    type: ActionTypes.MERGE_CURRENT_BOX_SCORES,
    boxScores: games
  }
}


export function updateBoxScore(gameId, teamId, points) {
  log.trace('actionsCurrentBoxScores.updateBoxScore')

  return {
    type: ActionTypes.UPDATE_CURRENT_BOX_SCORE,
    id: gameId,
    team: teamId,
    score: points
  }
}
