'use strict'

require('../../test-dom')()
import React from 'react'
import LiveLineupSelectModal from '../../../components/live/live-lineup-select-modal.jsx'
import { expect } from 'chai'
import sd from 'skin-deep';

const TestUtils = React.addons.TestUtils;


const lineupsSameSportProps = {
  lineups: [
  {
    "id": 1,
    "contest": 2,
    "lineup": 1,
    "title": "Curry's Chicken",
    "draft_group": 1,
    "start": "2015-10-15T23:00:00Z",
    "sport": "nba",
    "pts": 85,
    "pmr": 42
  },
  {
    "id": 2,
    "contest": 2,
    "lineup": 2,
    "title": "Worriers worry",
    "draft_group": 2,
    "start": "2015-10-15T23:00:00Z",
    "sport": "nba",
    "pts": 85,
    "pmr": 42
  },
  {
    "id": 3,
    "contest": 3,
    "lineup": 3,
    "title": "Kickass your jackass",
    "draft_group": 3,
    "start": "2015-10-15T23:00:00Z",
    "sport": "nba",
    "pts": 102,
    "pmr": 67
  }
  ]
}


const lineupsDifferentSportProps = {
  lineups: [
  {
    "id": 1,
    "contest": 2,
    "lineup": 1,
    "title": "Curry's Chicken",
    "draft_group": 1,
    "start": "2015-10-15T23:00:00Z",
    "sport": "nba",
    "pts": 85,
    "pmr": 42
  },
  {
    "id": 2,
    "contest": 2,
    "lineup": 2,
    "title": "Worriers worry",
    "draft_group": 2,
    "start": "2015-10-15T23:00:00Z",
    "sport": "nfl",
    "pts": 85,
    "pmr": 42
  },
  {
    "id": 3,
    "contest": 3,
    "lineup": 3,
    "title": "Kickass your jackass",
    "draft_group": 3,
    "start": "2015-10-15T23:00:00Z",
    "sport": "nba",
    "pts": 102,
    "pmr": 67
  }
  ]
}



describe('LiveLineupSelectModal Component', function() {

  describe('LiveLineupsSelectModal Component when all lineups with same sport', function () {
    let vdom, instance;

    beforeEach(function() {
      const tree = sd.shallowRender(React.createElement(LiveLineupSelectModal, lineupsSameSportProps))

      instance = tree.getMountedInstance()
      vdom = tree.getRenderOutput()

    })

    it('it should set state.selectedSport directly as all lineups same sport', function() {
      expect(instance.state.selectedSport).to.equal('nba')
    })

    it('title should be select lineup as we are directly on the lineup selection', function() {
      // I guess I'm supposed to do this with https://facebook.github.io/react/docs/test-utils.html
      const header = vdom.props.children.props.children.filter(prop => TestUtils.isElementOfType(prop, 'header'))[0]
      expect(header.props.children).to.equal('Choose a lineup')
    })

    it('should provide you with 3 lineups to choose from (according to props given)', function() {
      const content = vdom.props.children.props.children.filter(prop => TestUtils.isElementOfType(prop, 'div'))[0]
      expect(content.props.children.props.children.length).to.equal(3)
    })
  })

  describe('LiveLineupSelectModal Component when lineups are from different sports', function() {
    let vdom, instance;

    beforeEach(function() {
      const tree = sd.shallowRender(React.createElement(LiveLineupSelectModal, lineupsDifferentSportProps))

      instance = tree.getMountedInstance()
      vdom = tree.getRenderOutput()
    });

    it('it should set state.selectedSport to null as there is more than one sport', function() {
      expect(instance.state.selectedSport).to.equal(null)
    });

    it('title should be choose a sport as we have a sport yet to choose', function() {
      // I guess I'm supposed to do this with https://facebook.github.io/react/docs/test-utils.html
      const header = vdom.props.children.props.children.filter(prop => TestUtils.isElementOfType(prop, 'header'))[0]
      expect(header.props.children).to.equal('Choose a sport')
    })

    it('should provide you with 2 sports to choose from (according to props given)', function() {
      const content = vdom.props.children.props.children.filter(prop => TestUtils.isElementOfType(prop, 'div'))[0]
      expect(content.props.children.props.children.length).to.equal(2)
    })
  })

})
