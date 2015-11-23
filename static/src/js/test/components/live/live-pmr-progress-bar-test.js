'use strict';

require('../../test-dom')();
var React = require('react');
var ReactDOM = require('react-dom');
var LivePMRProgressBar = require('../../../components/live/live-pmr-progress-bar.jsx');
var expect = require('chai').expect;


// need to repeat the component with different data, so sadly can't use a beforeEach method
describe('LivePMRProgressBar Component', function() {

  it('should render an <svg>', function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = ReactDOM.render(
      <LivePMRProgressBar decimalRemaining="0.3" strokeWidth="2" backgroundHex="46495e" hexStart="34B4CC" hexEnd="2871AC" svgWidth="50" />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var pmrElement = ReactDOM.findDOMNode(this);
        expect(pmrElement.querySelectorAll('svg').length).to.be.above(0);
      }
    );
  });

});
