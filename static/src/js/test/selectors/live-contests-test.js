'use strict'

import request from 'superagent'
import sinon from 'sinon'
import { expect } from 'chai'
import { size as _size } from 'lodash'

import reducers from '../../reducers/index'
import urlConfig from '../../fixtures/entries-config'
import { fetchEntriesIfNeeded, addEntriesPlayers } from '../../actions/entries'
import { liveContestsStatsSelector } from '../../selectors/live-contests'
import { mockStore } from '../mock-store'


describe('selectorsLiveContests', () => {
  // setup mock urls
  before(function() {
    this.superagentMock = require('superagent-mock')(request, urlConfig)
  })

  // remove mock urls
  after(function() {
    this.superagentMock.unset()
  })


  it('should properly return data for liveContestsStatsSelector', (done) => {
    const store = mockStore(reducers, { entries: {} })

    store.dispatch(fetchEntriesIfNeeded()).then(() => {
      store.dispatch(addEntriesPlayers()).then(() => {
        var state = store.getState()

        var data = liveContestsStatsSelector(state)

        expect(data[0].stats[1].points).to.equal(71)

        done()
      })
    })
  })

})
