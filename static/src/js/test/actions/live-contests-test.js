'use strict'

import request from 'superagent'
import sinon from 'sinon'
import { expect } from 'chai'
import { size as _size } from 'lodash'

import reducers from '../../reducers/index'
import urlConfig from '../../fixtures/live-contests-config'
import { fetchContestIfNeeded, fetchRelatedContestInfo, generateContestStats } from '../../actions/live-contests'
import { mockStore } from '../mock-store'


describe('actionsLiveContests', () => {
  // setup mock urls
  before(function() {
    this.superagentMock = require('superagent-mock')(request, urlConfig)
  })

  // remove mock urls
  after(function() {
    this.superagentMock.unset()
  })


  it('should properly fetchContestIfNeeded on initial call', (done) => {
    const expectedActions = [
      // { type: '@@redux/INIT' }
      null,

      // requestLiveContestInfo
      function(action) {
        expect(action.type).to.equal('REQUEST_LIVE_CONTEST_INFO')
      },

      // receiveLiveContestInfo
      function(action) {
        expect(action.type).to.equal('RECEIVE_LIVE_CONTEST_INFO')
        expect(action.info.name).to.equal('NBA $5 Head-to-Head')
      },

      // requestLiveContestLineups
      function(action) {
        expect(action.type).to.equal('REQUEST_LIVE_CONTEST_LINEUPS')
      },

      // receiveLiveContestLineups
      function(action) {
        expect(action.type).to.equal('RECEIVE_LIVE_CONTEST_LINEUPS')
        expect(action.lineupBytes.length).to.equal(92)
      },

      // the end is from fetchRelatedContestInfo, tested in live draft groups
      null,
      null,
      null,
      null,
      null,
      null,

      // pull in prize information
      null,
      null
    ]

    const store = mockStore(reducers, {}, expectedActions, done)
    store.dispatch(fetchContestIfNeeded(2))
  })


  it('should not complete fetchContestIfNeeded if data already exists', (done) => {
    const expectedActions = [
      // { type: '@@redux/INIT' }
      null
    ]

    const store = mockStore(
      reducers,
      {
        liveContests: {
          2: {}
        }
      },
      expectedActions,
      done
    )

    store.dispatch(fetchContestIfNeeded(2))
  })


  it('should properly fetchRelatedContestInfo', (done) => {
    const expectedActions = [
      // { type: '@@redux/INIT' }
      null,

      null,
      null,
      null,
      null,
      null,

      // receiveLiveDraftGroupFP
      function(action) {
        expect(action.type).to.equal('RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES')
      },

      null,
      null

    ]

    const store = mockStore(
      reducers,
      {
        liveContests: {
          2: {
            info: {
              draft_group: 1
            }
          }
        }
      },
      expectedActions,
      done
    )
    store.dispatch(fetchRelatedContestInfo(2))
  })

})
