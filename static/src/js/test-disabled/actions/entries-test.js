'use strict'

import request from 'superagent'
import sinon from 'sinon'
import { expect } from 'chai'
import { size as _size } from 'lodash'

import reducers from '../../reducers/index'
import urlConfig from '../../fixtures/live-config'
import { fetchCurrentEntriesAndRelated, addEntriesPlayers } from '../../actions/entries'
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


  it('should properly fetchCurrentEntriesAndRelated on initial call', (done) => {
    const expectedActions = [
      // fetchCurrentEntriesAndRelated
      null,

      // requestEntries
      function(action) {
        expect(action.type).to.equal('ENTRIES__REQUEST')
      },

      // receiveEntries
      function(action) {
        expect(action.type).to.equal('ENTRIES__RECEIVE')
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
    store.dispatch(fetchCurrentEntriesAndRelated()).then(() => {
      done()
    })
  })


  it('should not complete fetchCurrentEntriesAndRelated if data already exists', (done) => {
    const expectedActions = [
      // fetchCurrentEntriesAndRelated
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

    store.dispatch(fetchCurrentEntriesAndRelated())
  })


  it('should not complete fetchCurrentEntriesAndRelated if data is currently being fetched', (done) => {
    const expectedActions = [
      // fetchCurrentEntriesAndRelated
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

    store.dispatch(fetchCurrentEntriesAndRelated())
  })


  it('should properly addEntriesPlayers', (done) => {
    const store = mockStore(reducers, {})

    store.dispatch(
      fetchCurrentEntriesAndRelated()
    ).then(() =>
      store.dispatch(addEntriesPlayers())
    ).then(() => {
      expect(store.getState().entries.items[1].roster.length).to.equal(8)
      done()
    })
  })
})
