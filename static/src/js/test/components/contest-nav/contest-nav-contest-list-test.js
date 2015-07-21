'use strict';

require('../../test-dom')();
var React = require('react/addons');
var ContestNavContestList = require('../../../components/contest-nav/contest-nav-contest-list.jsx');
var expect = require('chai').expect;


describe("ContestNavContestList Component", function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.componentComponent = React.render(
      <ContestNavContestList />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.componentElement = this.getDOMNode();
        done();
      }
    );
  });


  it("should render a div element", function() {
    expect(this.componentElement.tagName).to.equal('DIV');
  });

});
