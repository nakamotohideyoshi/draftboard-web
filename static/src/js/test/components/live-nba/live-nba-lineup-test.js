'use strict';

require('../../test-dom')();
var React = require('react/addons');
var LiveNBALineup = require('../../../components/live-nba/live-nba-lineup.jsx');
var expect = require('chai').expect;


describe('LiveNBALineup Component', function() {

  it('should render a <div>', function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = React.render(
      <LiveNBALineup />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var element = this.getDOMNode();
        expect(element.tagName).to.equal('DIV');
      }
    );
  });


  // TODO change this to be async
  it("should render players by default", function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = React.render(
      <LiveNBALineup />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var element = this.getDOMNode();
        expect(element.querySelectorAll('.live-lineup-player').length).to.be.above(0);
      }
    );
  });


  // TODO change this to be async
  it("should adjust class if whichSide is `me`", function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = React.render(
      <LiveNBALineup whichSide="me" />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var element = this.getDOMNode();
        expect(element.getAttribute('class')).to.contain('live-lineup--me');
      }
    );
  });
});
