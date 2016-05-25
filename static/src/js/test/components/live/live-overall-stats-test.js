'use strict';

require('../../test-dom')();
var React = require('react');
var ReactDOM = require('react-dom');
import LiveOverallStats from '../../../components/live/live-overall-stats.jsx';
var expect = require('chai').expect;

const defaultProps = {
  whichSide: "me",
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
  hasContest: true,
  lineup: {
    id: 3,
    name: 'villy17',
    points: 72,
    earnings: '$100',
    progress: 74,
    timeRemaining: { decimal: 0.5 },
    potentialWinnings: 2.123123,
  },
};

// need to repeat the component with different data, so sadly can't use a beforeEach method
describe('LiveOverallStats Component', function() {

  it('should render an endpoint circle', function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = ReactDOM.render(
      React.createElement(LiveOverallStats, defaultProps),
      this.targetElement = document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        expect(self.targetElement.querySelectorAll('.progress-endpoint').length).to.be.above(0);
      }
    );
  });
});
