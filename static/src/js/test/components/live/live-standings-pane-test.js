'use strict'

require('../../test-dom')()

import React from 'react'
import ReactDOM from 'react-dom'
import ReactTestUtils from 'react-addons-test-utils'
import {expect} from 'chai'

import {LiveStandingsPane} from '../../../components/live/live-standings-pane'

const defaultProps = {
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
  lineups: [
    {
      id: 1,
      name: 'villy17',
      points: 72,
      earnings: '$100',
      progress: 74
    },
    {
      id: 2,
      name: 'villy18',
      points: 71,
      earnings: '$90',
      progress: 31
    }
  ]
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
      this.componentElement.querySelector('.live-standings-pane__header .title:not(.active)')
    );

    expect(
      this.componentElement.querySelectorAll('.standings-list').length
    ).to.equal(0);
    expect(
      this.componentElement.querySelectorAll('.ownership-list').length
    ).to.equal(1);

    ReactTestUtils.Simulate.click(
      this.componentElement.querySelector('.live-standings-pane__header .title:not(.active)')
    );

    expect(
      this.componentElement.querySelectorAll('.standings-list').length
    ).to.equal(1);
    expect(
      this.componentElement.querySelectorAll('.ownership-list').length
    ).to.equal(0);
  });

  it('should should be able to filter players by position', function() {
    // Show ownership tab.
    ReactTestUtils.Simulate.click(
      this.componentElement.querySelector('.live-standings-pane__header .title:not(.active)')
    );

    expect(
      this.componentElement.querySelectorAll('.player').length
    ).to.equal(2);

    ReactTestUtils.Simulate.click(
      this.componentElement.querySelector('.position-filter.pg')
    );

    expect(
      this.componentElement.querySelectorAll('.player').length
    ).to.equal(1);

    ReactTestUtils.Simulate.click(
      this.componentElement.querySelector('.position-filter.pf')
    );

    expect(
      this.componentElement.querySelectorAll('.player').length
    ).to.equal(0);

    ReactTestUtils.Simulate.click(
      this.componentElement.querySelector('.position-filter.c')
    );

    expect(
      this.componentElement.querySelectorAll('.player').length
    ).to.equal(1);

    ReactTestUtils.Simulate.click(
      this.componentElement.querySelector('.position-filter.all')
    );

    expect(
      this.componentElement.querySelectorAll('.player').length
    ).to.equal(2);
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
      ).to.equal(1);

      expect(
        this.componentElement.querySelector('.lineup--place').innerHTML.trim()
      ).to.equal('1');

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
