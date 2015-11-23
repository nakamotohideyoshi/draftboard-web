'use strict'

import request from 'superagent'
import sinon from 'sinon'
import { expect } from 'chai'
import { size as _size } from 'lodash'

import reducers from '../../reducers/index'
import urlConfig from '../../fixtures/live-config'
import { setCurrentLineups } from '../../actions/current-lineups'
import { mockStore } from '../mock-store'
import { fetchEntriesIfNeeded, generateLineups } from '../../actions/entries'


describe('actionsCurrentLineups', () => {
  // setup mock urls
  before(function() {
    this.superagentMock = require('superagent-mock')(request, urlConfig)
  })

  // remove mock urls
  after(function() {
    this.superagentMock.unset()
  })


  // it('should properly setCurrentLineups', (done) => {
  //   const expectedActions = [
  //     // { type: '@@redux/INIT' }
  //     null,

  //     // setCurrentLineups
  //     function(action, state) {
  //       expect(action.type).to.equal('SET_CURRENT_LINEUPS')
  //       expect(state.currentLineups.lineups.length).to.equal(1)
  //     }
  //   ]

  //   const store = mockStore(reducers, {}, expectedActions, done)
  //   store.dispatch(setCurrentLineups([
  //     {
  //       "id": 1,
  //       "name": "Curry's Chicken",
  //       "start": "2015-10-15T23:00:00Z",
  //       "draft_group": 1
  //     }
  //   ]))
  // })


  it('should properly setCurrentLineups based on data from entries', (done) => {
    const store = mockStore(reducers, { entries: {} })
    store.dispatch(fetchEntriesIfNeeded()).then(() => {
      store.dispatch(generateLineups()).then(() => {
        expect(store.getState().currentLineups.items[0].id).to.equal(1)
        done()
      })

    })
  })


})
