'use strict'

require('../../test-dom')();

import React from 'react';
import { LiveChooseLineup } from '../../../components/live/live-choose-lineup';
import { expect } from 'chai';
import sd from 'skin-deep';
import { merge as _merge } from 'lodash';

import reducers from '../../../reducers/index';
import { mockStore } from '../../mock-store';

import ReactTestUtils from 'react-addons-test-utils';

const lineupsSameSportProps = {
  entriesLoaded: true,
  changePathAndMode() {},
  entries: [
    {
      "id": 1,
      "draftGroup": {
        "id": 1
      },
      "contest": 2,
      "lineup": 1,
      "name": "Curry's Chicken",
      "start": "2015-10-15T23:00:00Z",
      "sport": "nba",
      "points": 85,
      "minutesRemaining": 42
    }, {
      "id": 2,
      "contest": 2,
      "lineup": 2,
      "name": "Worriers worry",
      "draftGroup": {
        "id": 2
      },
      "start": "2015-10-15T23:00:00Z",
      "sport": "nba",
      "points": 85,
      "minutesRemaining": 42
    }, {
      "id": 3,
      "contest": 3,
      "lineup": 3,
      "name": "Kickass your jackass",
      "draftGroup": {
        "id": 3
      },
      "start": "2015-10-15T23:00:00Z",
      "sport": "nba",
      "points": 102,
      "minutesRemaining": 67
    }
  ]
};


const lineupsDifferentSportProps = {
  entriesLoaded: true,
  changePathAndMode() {},
  entries: [
    {
      "id": 1,
      "draftGroup": {
        "id": 1
      },
      "contest": 2,
      "lineup": 1,
      "name": "Curry's Chicken",
      "start": "2015-10-15T23:00:00Z",
      "sport": "nba",
      "points": 85,
      "minutesRemaining": 42
    },
    {
      "id": 2,
      "contest": 2,
      "lineup": 2,
      "name": "Worriers worry",
      "draftGroup": {
        "id": 2
      },
      "start": "2015-10-15T23:00:00Z",
      "sport": "mlb",
      "points": 85,
      "minutesRemaining": 42
    },
    {
      "id": 3,
      "contest": 3,
      "lineup": 3,
      "name": "Kickass your jackass",
      "draftGroup": {
        "id": 3
      },
      "start": "2015-10-15T23:00:00Z",
      "sport": "nfl",
      "points": 102,
      "minutesRemaining": 67
    },
  ]
};


describe('LiveChooseLineup Component', function() {

  describe('LiveLineupsSelectModal Component when all lineups with same sport', function () {
    let vdom, instance;

    beforeEach(function() {
      const store = mockStore(reducers, {});
      const props = lineupsSameSportProps;
      const tree = sd.shallowRender(React.createElement(LiveChooseLineup, props));

      instance = tree.getMountedInstance();
      vdom = tree.getRenderOutput();
    });

    it('title should be select lineup as we are directly on the lineup selection', function() {
      // I guess I'm supposed to do this with https://facebook.github.io/react/docs/test-utils.html
      const header = vdom.props.children.props.children
              .filter(prop => ReactTestUtils.isElementOfType(prop, 'header'))[0];
      expect(header.props.children).to.equal('Choose a lineup');
    })

    it('should provide you with 3 lineups to choose from (according to props given)', function() {
      const content = vdom.props.children.props.children
              .filter(prop => ReactTestUtils.isElementOfType(prop, 'div'))[0];
      expect(content.props.children.props.children.length).to.equal(3);
    })
  })

  describe('LiveChooseLineup Component when lineups are from different sports', function() {
    let vdom, instance;

    beforeEach(function() {
      const store = mockStore(reducers, {});
      const props = lineupsDifferentSportProps;
      const tree = sd.shallowRender(React.createElement(LiveChooseLineup, props));

      instance = tree.getMountedInstance();
      vdom = tree.getRenderOutput();
    });

    it('it should set state.selectedSport to null as there is more than one sport', function() {
      expect(instance.state.selectedSport).to.equal(null);
    });

    it('title should be choose a sport as we have a sport yet to choose', function() {
      // I guess I'm supposed to do this with https://facebook.github.io/react/docs/test-utils.html
      const header = vdom.props.children.props.children
              .filter(prop => ReactTestUtils.isElementOfType(prop, 'header'))[0];
      expect(header.props.children).to.equal('Choose a sport');
    })

    it('should provide you with 3 sports to choose from (according to props given)', function() {
      const content = vdom.props.children.props.children
              .filter(prop => ReactTestUtils.isElementOfType(prop, 'div'))[0];
      expect(content.props.children.props.children.length).to.equal(3);
    })
  })

})
