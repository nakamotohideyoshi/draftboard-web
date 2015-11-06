'use strict'

import request from 'superagent'
import sinon from 'sinon'
import { expect } from 'chai'
import { size as _size } from 'lodash'

import reducersEntries from '../../reducers/entries'
import urlConfig from '../../fixtures/entries-config'
import { fetchEntriesIfNeeded } from '../../actions/entries'
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
        expect(_size(action.items)).to.equal(10)
      }
    ]

    const store = mockStore(reducersEntries, { entries: {} }, expectedActions, done)
    store.dispatch(fetchEntriesIfNeeded())
  })


  it('should not complete fetchEntriesIfNeeded if data already exists', (done) => {
    const expectedActions = [
      // fetchEntriesIfNeeded
      null
    ]

    const store = mockStore(
      reducersEntries,
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
      reducersEntries,
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

})
