'use strict'

import request from 'superagent'
import sinon from 'sinon'
import { expect } from 'chai'
import { size as _size } from 'lodash'

import reducers from '../../reducers/index'
import urlConfig from '../../fixtures/live-config'
import { fetchPrizeIfNeeded } from '../../actions/prizes'
import { mockStore } from '../mock-store'


describe('actionsLivePrizes', () => {
  // setup mock urls
  before(function() {
    this.superagentMock = require('superagent-mock')(request, urlConfig)
  })

  // remove mock urls
  after(function() {
    this.superagentMock.unset()
  })


  it('should properly fetchPrizeIfNeeded on initial call', (done) => {
    const expectedActions = [
      // fetchPrizeIfNeeded
      null,

      // requestLivePrize
      function(action) {
        expect(action.type).to.equal('REQUEST_PRIZE')
      },

      // receiveLivePrize
      function(action) {
        expect(action.type).to.equal('RECEIVE_PRIZE')
        expect(action.info.name).to.equal('new prize structure')
      }

    ]

    const store = mockStore(reducers, {}, expectedActions, done)
    store.dispatch(fetchPrizeIfNeeded(1))
  })


  it('should not complete fetchPrizeIfNeeded if data already exists', (done) => {
    const expectedActions = [
      // fetchPrizeIfNeeded
      null
    ]

    const store = mockStore(
      reducers,
      {
        prizes: {
          1: {}
        }
      },
      expectedActions,
      done
    )

    store.dispatch(fetchPrizeIfNeeded(1))
  })

})
