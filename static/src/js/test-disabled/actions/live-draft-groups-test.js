'use strict'

import request from 'superagent'
import sinon from 'sinon'
import { combineReducers } from 'redux'
import { expect } from 'chai'
import size from 'lodash/size';

import reducers from '../../reducers/index'
import urlConfig from '../../fixtures/live-config'
import { fetchDraftGroupIfNeeded } from '../../actions/live-draft-groups'
import { mockStore } from '../mock-store'
// import store from '../../store'


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
      // { type: '@@redux/INIT' }
      null,

      // requestLiveDraftGroup
      function(action, state) {
        expect(action.type).to.equal('LIVE_DRAFT_GROUP__INFO__REQUEST')
      },

      // receiveLiveDraftGroup
      function(action) {
        expect(action.type).to.equal('LIVE_DRAFT_GROUP__INFO__RECEIVE')
        expect(size(action.players)).to.equal(74)
      },

      // requestLiveDraftGroupFP
      function(action) {
        expect(action.type).to.equal('REQUEST_LIVE_DRAFT_GROUP_FP')
      },

      // receiveLiveDraftGroupFP
      function(action, state) {
        expect(action.type).to.equal('RECEIVE_LIVE_DRAFT_GROUP_FP')
        expect(action.players[1].fp).to.equal(3.5)
      },

      function(action) {
        expect(action.type).to.equal('REQUEST_LIVE_DRAFT_GROUP_BOX_SCORES')
      },

      function(action) {
        expect(action.type).to.equal('RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES')
        expect(action.boxScores['cf9a5e4d-9487-4daf-bebc-5897f86d9199'].pk).to.equal(55)
      }
    ]

    const store = mockStore(reducers, {}, expectedActions, done)
    store.dispatch(fetchDraftGroupIfNeeded(1))
  })


  it('should not complete fetchDraftGroupIfNeeded if data already exists', (done) => {
    const expectedActions = [
      // { type: '@@redux/INIT' }
      null
    ]

    const store = mockStore(
      reducers,
      {
        liveDraftGroups: {
          1: {}
        }
      },
      expectedActions,
      done
    )

    store.dispatch(fetchDraftGroupIfNeeded(1))
  })

})
