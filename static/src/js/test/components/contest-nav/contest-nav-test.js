'use strict';

require('../../test-dom')();
var React = require('react/addons');
var ContestNav = require('../../../components/contest-nav/contest-nav.jsx');
var expect = require('chai').expect;


describe("ContestNav Component", function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.contestNavComponent = React.render(
      <ContestNav />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.contestNavElement = this.getDOMNode();
        done();
      }
    );
  });


  afterEach(function() {
    document.body.innerHTML = '';
  });


  it('should render a div tag and a list component', function() {
    expect(this.contestNavElement.tagName).to.equal('DIV');
    expect(
      this.contestNavElement.querySelectorAll('.cmp-contest-nav--contests-list').length
    ).to.equal(1);
  });


  it("should render the ContestNavFilters and ContestNavContestList components", function() {
    expect(
      this.contestNavElement.querySelectorAll('.cmp-contest-nav--filters').length
      ).to.equal(1);

    expect(
      this.contestNavElement.querySelectorAll('.cmp-contest-nav--contests').length
      ).to.equal(1);
  });

});
