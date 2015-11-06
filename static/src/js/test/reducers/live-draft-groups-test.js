'use strict'

import request from 'superagent'
import sinon from 'sinon'
import { expect } from 'chai'
import { size as _size } from 'lodash'

import reducersLiveDraftGroups from '../../reducers/live-draft-groups'
import urlConfig from '../../fixtures/live-draft-groups-config'
import { fetchDraftGroupIfNeeded } from '../../actions/live-draft-groups'
import { mockStore } from '../mock-store'


describe('actionsLiveDraftGroups', () => {
  // setup mock urls
  before(function() {
    this.superagentMock = require('superagent-mock')(request, urlConfig)
  })

  // remove mock urls
  after(function() {
    this.superagentMock.unset()
  })


  it('should properly fetchDraftGroupIfNeeded on initial call', (done) => {
    const expectedActions = [
      // fetchDraftGroupIfNeeded
      null,

      // requestLiveDraftGroup
      function(action) {
        expect(action.type).to.equal('REQUEST_LIVE_DRAFT_GROUP_INFO')
      },

      // receiveLiveDraftGroup
      function(action) {
        expect(action.type).to.equal('RECEIVE_LIVE_DRAFT_GROUP_INFO')
        expect(_size(action.players)).to.equal(79)
      },

      // requestLiveDraftGroupFP
      function(action) {
        expect(action.type).to.equal('REQUEST_LIVE_DRAFT_GROUP_FP')
      },

      // receiveLiveDraftGroupFP
      function(action) {
        expect(action.type).to.equal('RECEIVE_LIVE_DRAFT_GROUP_FP')
        expect(action.playersFP[1].fp).to.equal(3.5)
      }
    ]

    const store = mockStore(reducersLiveDraftGroups, {}, expectedActions, done)
    store.dispatch(fetchDraftGroupIfNeeded(1))
  })


  it('should not complete fetchDraftGroupIfNeeded if data already exists', (done) => {
    const expectedActions = [
      // fetchDraftGroupIfNeeded
      null
    ]

    const store = mockStore(
      reducersLiveDraftGroups,
      {
        1: {}
      },
      expectedActions,
      done
    )

    store.dispatch(fetchDraftGroupIfNeeded(1))
  })

})
