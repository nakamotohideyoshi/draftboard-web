'use strict';

require('../../test-dom')();
var React = require('react');
var ReactDOM = require('react-dom');
var LiveOverallStats = require('../../../components/live/live-overall-stats.jsx');
var expect = require('chai').expect;


// need to repeat the component with different data, so sadly can't use a beforeEach method
describe('LiveOverallStats Component', function() {

  it('should render an endpoint circle', function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = ReactDOM.render(
      <LiveOverallStats whichSide="me" />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var pmrElement = ReactDOM.findDOMNode(this);
        expect(pmrElement.querySelectorAll('.progress-endpoint').length).to.be.above(0);
      }
    );
  });


  // TODO pass in real data for the overall stats percentage
  // it('should render a hex halfway in between', function() {
  //   var self = this;

  //   // Render the component into our fake jsdom element.
  //   this.sectionComponent = ReactDOM.render(
  //     <LiveNBAPMRProgressBar diameter="220" strokeWidth="2" percentComplete="50" startHex="000000" endHex="222222" showEndpoint="True" backgroundHex="0c0d14" />,
  //     document.body.appendChild(document.createElement('div')),
  //     function() {
  //       // Once it has been rendered, grab it from the DOM.
  //       var pmrElement = ReactDOM.findDOMNode(this);
  //       expect(pmrElement.querySelector('.progress-endpoint circle').getAttribute('stroke')).to.equal('#111111');
  //     }
  //   );
  // });

});
