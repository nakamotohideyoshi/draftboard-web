"use strict";

require("../../test-dom")();
var assert = require("assert");
var React = require("react");
var ReactDOM = require('react-dom');
var LiveHistory = require("../../../components/live-nba/live-nba-history.jsx");
var fixtures = require('../../../fixtures/live-nba-history')[0].fixtures();
var expect = require('chai').expect;


describe("LiveHistory Component", function() {

  it("should render a div tag", function() {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.liveHistoryComponent = ReactDOM.render(
      <LiveHistory data={fixtures} />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.liveHIstoryElement = ReactDOM.findDOMNode(this);
        assert.equal(self.liveHIstoryElement.tagName, "DIV");
      }
    );


  });


  it("should render all of the events as <div>'s", function() {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.liveHistoryComponent = ReactDOM.render(
      <LiveHistory data={fixtures} />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.liveHIstoryElement = ReactDOM.findDOMNode(this);
        expect(self.liveHIstoryElement.querySelectorAll('.live-history__event').length).to.equal(fixtures.length);
      }
    );
  });


  it("should not render events if no data passed", function() {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.liveHistoryComponent = ReactDOM.render(
      <LiveHistory />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.liveHIstoryElement = ReactDOM.findDOMNode(this);
        expect(self.liveHIstoryElement.querySelectorAll('.live-history__event').length).to.equal(0);
      }
    );
  });


});
