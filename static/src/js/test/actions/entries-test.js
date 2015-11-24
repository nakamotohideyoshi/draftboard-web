'use strict'

import request from 'superagent'
import sinon from 'sinon'
import { expect } from 'chai'
import { size as _size } from 'lodash'

import reducers from '../../reducers/index'
import urlConfig from '../../fixtures/live-config'
import { fetchEntriesIfNeeded, addEntriesPlayers } from '../../actions/entries'
import { mockStore } from '../mock-store'


describe('actionsEntries', () => {
  // setup mock urls
  before(function() {
    this.superagentMock = require('superagent-mock')(request, urlConfig)
  })

  // remove mock urls
  after(function() {
    this.superagentMock.unset()
  })


  it('should properly fetchEntriesIfNeeded on initial call', (done) => {
    const expectedActions = [
      // fetchEntriesIfNeeded
      null,

      // requestEntries
      function(action) {
        expect(action.type).to.equal('REQUEST_ENTRIES')
      },

      // receiveEntries
      function(action) {
        expect(action.type).to.equal('RECEIVE_ENTRIES')
        expect(_size(action.items)).to.equal(1)
      },

      // to pull in the related contest information and fantasy points
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,
      null,

      // confirm that related data exists here
      function(action, state) {
        // TODO craig - write test for confirming data in entries
        // console.log(action.type)
      }
    ]

    const store = mockStore(reducers, { entries: {} }, expectedActions)
    store.dispatch(fetchEntriesIfNeeded()).then(() => {
      done()
    })
  })


  it('should not complete fetchEntriesIfNeeded if data already exists', (done) => {
    const expectedActions = [
      // fetchEntriesIfNeeded
      null
    ]

    const store = mockStore(
      reducers,
      {
        entries: {
          items: ['foo', 'bar']
        }
      },
      expectedActions,
      done
    )

    store.dispatch(fetchEntriesIfNeeded())
  })


  it('should not complete fetchEntriesIfNeeded if data is currently being fetched', (done) => {
    const expectedActions = [
      // fetchEntriesIfNeeded
      null
    ]

    const store = mockStore(
      reducers,
      {
        entries: {
          isFetching: true
        }
      },
      expectedActions,
      done
    )

    store.dispatch(fetchEntriesIfNeeded())
  })


  it('should properly addEntriesPlayers', (done) => {
    const store = mockStore(reducers, {})

    store.dispatch(
      fetchEntriesIfNeeded()
    ).then(() =>
      store.dispatch(addEntriesPlayers())
    ).then(() => {
      expect(store.getState().entries.items[1].roster.length).to.equal(8)
      done()
    })
  })
})
