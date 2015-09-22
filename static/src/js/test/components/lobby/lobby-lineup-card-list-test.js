'use strict';

require('../../test-dom')();
var assert = require('assert');
var React = require('react/addons');
var Component = require('../../../components/lobby/lobby-lineup-card-list.jsx');
// var expect = require('chai').expect;


describe("LobbyLineupCardList Component", function() {

  beforeEach(function(done) {
    var self = this;

    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.component = React.render(
      <Component />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.domElement = this.getDOMNode();
        done();
      }
    );
  });


  afterEach(function() {
    // Remove component from the DOM and empty the DOM for good measure.
    //
    // These suckers don't clean up nicely, so ignore this for now.
    // React.unmountComponentAtNode(this.targetElement);
    document.body.innerHTML = '';
  });


  it("should render a div tag", function() {
    assert.equal(this.domElement.tagName, 'DIV');
  });

});
