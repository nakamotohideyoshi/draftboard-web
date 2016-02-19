'use strict';

require('../../test-dom')();
const React = require('react');
const ReactDOM = require('react-dom');
const ResultsStats = require('../../../components/results/results-stats.jsx');
const expect = require('chai').expect;

const defaultProps = {
  stats: {
    winnings: "$101",
    possible: "$512.4",
    fees:     "$359",
    entries:  18,
    contests: 8
  }
};

describe("ResultsStats Component", function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.component = ReactDOM.render(
      React.createElement(ResultsStats, defaultProps),
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.componentElement = ReactDOM.findDOMNode(this);
        done();
      }
    );
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  it('should render all provided stats', function() {
    expect(this.componentElement.tagName).to.equal('DIV');

    expect(
      this.componentElement.querySelector('.winnings .value').textContent.trim()
    ).to.equal(defaultProps.stats.winnings);

    expect(
      this.componentElement.querySelector('.possible .value').textContent.trim()
    ).to.equal(defaultProps.stats.possible);

    expect(
      this.componentElement.querySelector('.fees .value').textContent.trim()
    ).to.equal(defaultProps.stats.fees);

    expect(
      this.componentElement.querySelector('.entries .value').textContent.trim()
    ).to.equal(defaultProps.stats.entries.toString());

    expect(
      this.componentElement.querySelector('.contests .value').textContent.trim()
    ).to.equal(defaultProps.stats.contests.toString());
  });

});
