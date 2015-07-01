"use strict";

require("../test-dom")();
var assert = require("assert");
var React = require("react/addons");
var TestUtils = React.addons.TestUtils;
var ContestListComponent = require("../../components/contest-list/contest-list.jsx");


describe("ContestListComponent", function() {

  beforeEach(function() {
    // Render the component into our fake jsdom.
    this.contestListComponent = TestUtils.renderIntoDocument(<ContestListComponent />);
    // Grab it.
    this.contestListElement = this.contestListComponent.getDOMNode();
  });

  afterEach(function() {
    // Remove component from the DOM.
    React.unmountComponentAtNode(this.contestListElement);
  });

  it("should render a table tag", function() {
    assert.equal(this.contestListElement.tagName, "TABLE");
  });

  it("should render all of the contests as TR's", function() {
    assert.equal(this.contestListElement.getElementsByTagName("tr").length, 7);
  });

});
