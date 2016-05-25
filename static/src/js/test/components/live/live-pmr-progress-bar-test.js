'use strict';

require('../../test-dom')();
var React = require('react');
var ReactDOM = require('react-dom');
import LivePMRProgressBar from '../../../components/live/live-pmr-progress-bar.jsx';
var expect = require('chai').expect;


// need to repeat the component with different data, so sadly can't use a beforeEach method
describe('LivePMRProgressBar Component', function() {

  it('should render an <svg>', function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = ReactDOM.render(
      <LivePMRProgressBar id="1" decimalRemaining={0.3} strokeWidth={2} backgroundHex="46495e" hexStart="34B4CC" hexEnd="2871AC" svgWidth={50} />,
      this.targetElement = document.body.appendChild(document.createElement('div')),
      function() {
        expect(self.targetElement.querySelectorAll('svg').length).to.be.above(0);
      }
    );
  });

});
