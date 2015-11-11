"use strict"

import request from 'superagent'
import { normalize, Schema, arrayOf } from 'normalizr'

import log from '../lib/logging'
import { fetchEntriesIfNeeded } from './entries'
import { fetchDraftGroupIfNeeded } from './live-draft-groups'


export const SET_CURRENT_LINEUPS = 'SET_CURRENT_LINEUPS'


export function setCurrentLineups(lineups) {
  log.debug('actionsCurrentLineups.setCurrentLineups')

  return {
    type: SET_CURRENT_LINEUPS,
    lineups: lineups,
    updatedAt: Date.now()
  }
}
