'use strict'

import request from 'superagent'
import sinon from 'sinon'
import { expect } from 'chai'
import { size as _size } from 'lodash'

import reducers from '../../reducers/index'
import urlConfig from '../../fixtures/live-config'
import { fetchCurrentEntriesAndRelated, addEntriesPlayers } from '../../actions/entries'
import { myCurrentLineupsSelector } from '../../selectors/current-lineups'
import { mockStore } from '../mock-store'


describe('selectorsLiveLineups', () => {
  // setup mock urls
  before(function() {
    this.superagentMock = require('superagent-mock')(request, urlConfig)
  })

  // remove mock urls
  after(function() {
    this.superagentMock.unset()
  })


  it('should properly return data for myCurrentLineupsSelector', (done) => {
    const store = mockStore(reducers, { entries: {} })

    store.dispatch(fetchCurrentEntriesAndRelated()).then(() => {
      store.dispatch(addEntriesPlayers()).then(() => {
        var state = store.getState()
        var data = myCurrentLineupsSelector(state)

        // TODO finish checking data

        done()
      })
    })
  })

})
