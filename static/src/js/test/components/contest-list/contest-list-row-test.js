"use strict";

require("../../test-dom")();
var assert = require("assert");
var React = require("react/addons");
var Component = require("../../../components/contest-list/contest-list-row.jsx");
var expect = require('chai').expect;


describe("ContestListRow Component", function() {

  beforeEach(function(done) {
    var props = {
      row: {'id': 8}
    };

    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('table'));
    // Render the component into our fake jsdom element.
    this.component = React.render(
      <Component row={props.row}/>,
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


  it("should render a tr tag", function() {
    assert.equal(this.domElement.tagName, "TR");
  });


  it("addLeadingZero() should add leading zeroes", function() {
    // Cast them as strings since eslint goes bonkers about an octal 0.
    expect(
      (this.component.addLeadingZero(2)).toString()
    ).to.equal(
      ('02').toString()
    );
  });

});
