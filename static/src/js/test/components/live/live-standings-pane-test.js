'use strict'

require('../../test-dom')()

import React from 'react';
import ReactDOM from 'react-dom';
import ReactTestUtils from 'react-addons-test-utils';
import { expect } from 'chai';

import { LiveStandingsPane } from '../../../components/live/live-standings-pane';

const defaultProps = {
  actions: {},
  changePathAndMode() {},
  contest: {
    id: 2,
    potentialWinnings: {
      amount: 2,
      percent: 2
    },
    playersOwnership: {
      all: [],
    },
    lineupsUsernames: {}
  },
  openOnStart: true,
  rankedLineups: [2, 3],
  watching: {},
  contestId: 2,
  owned: [
    {
      id: 1,
      name: 'Kobe Bryant',
      team: 'LAL',
      points: 72,
      position: 'pg',
      iamge: '',
      progress: 100
    },
    {
      id: 2,
      name: 'Kobe Bryant',
      team: 'LAL',
      points: 12,
      position: 'c',
      iamge: '',
      progress: 30
    }
  ],
  lineups: {
    3: {
      id: 3,
      name: 'villy17',
      points: 72,
      earnings: '$100',
      progress: 74,
      timeRemaining: { decimal: 0.5 },
      potentialWinnings: 2.123123,
    },
    2: {
      id: 2,
      name: 'villy18',
      points: 71,
      earnings: '$90',
      progress: 31,
      timeRemaining: { decimal: 0.5 },
      potentialWinnings: 2.123123,
    }
  }
}

describe("LiveStandingsPane Component", function() {

  beforeEach(function(done) {
    var self = this
    document.body.innerHTML = ''
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'))
    // Render the component into our fake jsdom element.
    this.component = ReactDOM.render(
      React.createElement(LiveStandingsPane, defaultProps),
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.componentElement = ReactDOM.findDOMNode(this)
        done()
      }
    )
  })

  afterEach(function() {
    document.body.innerHTML = ''
  })

  it('should render a div', function() {
    expect(this.componentElement.tagName).to.equal('DIV')
  })

  it('should should be able to switch tabs', function() {
    expect(
      this.componentElement.querySelectorAll('.standings-list').length
    ).to.equal(1);
    expect(
      this.componentElement.querySelectorAll('.ownership-list').length
    ).to.equal(0);

    ReactTestUtils.Simulate.click(
      this.componentElement.querySelector('.live-standings-pane__header .menu .title:not(.active)')
    );

    expect(
      this.componentElement.querySelectorAll('.standings-list').length
    ).to.equal(0);
    expect(
      this.componentElement.querySelectorAll('.ownership-list').length
    ).to.equal(1);

    ReactTestUtils.Simulate.click(
      this.componentElement.querySelector('.live-standings-pane__header .menu .title:not(.active)')
    );

    expect(
      this.componentElement.querySelectorAll('.standings-list').length
    ).to.equal(1);
    expect(
      this.componentElement.querySelectorAll('.ownership-list').length
    ).to.equal(0);
  });

  it('should should be able to work with pages', function() {
    expect(
      this.componentElement.querySelectorAll('.lineup').length
    ).to.equal(2);

    this.component.setState({perPage: 1});
    expect(this.component.getMaxPage()).to.equal(2);

    setTimeout(() => {
      expect(
        this.componentElement.querySelectorAll('.lineup').length
      ).to.equal(2);

      expect(
        this.componentElement.querySelector('.lineup--place').innerHTML.trim()
      ).to.equal('');

      ReactTestUtils.Simulate.click(
        this.componentElement.querySelector('.arrow-right')
      );

      expect(this.component.state.page).to.equal(2);

      expect(
        this.componentElement.querySelector('.lineup--place').innerHTML.trim()
      ).to.equal('2');

      ReactTestUtils.Simulate.click(
        this.componentElement.querySelector('.arrow-left')
      );

      expect(
        this.componentElement.querySelector('.lineup--place').innerHTML.trim()
      ).to.equal('1');
    }, 10)
  });
})
