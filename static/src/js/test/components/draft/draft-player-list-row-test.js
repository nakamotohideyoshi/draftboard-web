'use strict';

require('../../test-dom')();
var assert = require('assert');
var React = require('react');
var Component = require('../../../components/draft/draft-player-list-row.jsx');
// var expect = require('chai').expect;


describe("DraftPlayerListRow Component", function() {
  var component;
  var domElement;
  var targetElement;
  var props = {
    row: {
      'player_id': 7,
      'salary': 234987,
      'fppg': 23.888
    }
  };


  var renderComponent = function(done) {
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    targetElement = document.body.appendChild(document.createElement('table'));
    // Render the component into our fake jsdom element.
    component = React.render(
      <Component row={props.row} />,
      targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        domElement = this.getDOMNode();
        done();
      }
    );
  };


  beforeEach(function(done) {
    renderComponent(done);
  });


  afterEach(function() {
    // Remove component from the DOM and empty the DOM for good measure.
    //
    // These suckers don't clean up nicely, so ignore this for now.
    // React.unmountComponentAtNode(this.targetElement);
    document.body.innerHTML = '';
  });


  it("should render a tr tag", function() {
    assert.equal(domElement.tagName, 'TR');
  });

});
