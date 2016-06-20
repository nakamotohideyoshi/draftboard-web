'use strict'

import request from 'superagent'
import sinon from 'sinon'
import { expect } from 'chai'
import size from 'lodash/size';

import reducers from '../../reducers/index'
import urlConfig from '../../fixtures/live-config'
import { fetchCurrentEntriesAndRelated, addEntriesPlayers } from '../../actions/entries'
import { myLiveContestsSelector } from '../../selectors/live-contests'
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


  it('should properly return data for myLiveContestsSelector', (done) => {
    const store = mockStore(reducers, { entries: {} })

    store.dispatch(fetchCurrentEntriesAndRelated()).then(() => {
      var state = store.getState()
      var data = myLiveContestsSelector(state)

      expect(data[2].entriesStats[1].points).to.equal(71)

      done()
    })
  })

})
