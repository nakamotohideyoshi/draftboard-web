'use strict';

require('../../test-dom')();
const React = require('react');
const ReactDOM = require('react-dom');
const ContestNav = require('../../../components/contest-nav/contest-nav.jsx');
const expect = require('chai').expect;

const {TYPE_SELECT_GAMES, TYPE_SELECT_LINEUPS} = ContestNav;

describe("ContestNav Component", function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.contestNavComponent = ReactDOM.render(
      <ContestNav />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.contestNavElement = ReactDOM.findDOMNode(this);
        done();
      }
    );
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  it('should render a div tag, menu, user info, filters, slider and logo', function() {
    expect(this.contestNavElement.tagName).to.equal('DIV');
    expect(
      this.contestNavElement.querySelectorAll('.cmp-contest-nav--menu').length
    ).to.equal(1);
    expect(
      this.contestNavElement.querySelectorAll('.cmp-contest-nav--user-info').length
    ).to.equal(1);
    expect(
      this.contestNavElement.querySelectorAll('.cmp-contest-nav--filters').length
    ).to.equal(1);
    expect(
      this.contestNavElement.querySelectorAll('.cmp-contest-nav--slider').length
    ).to.equal(1);
    expect(
      this.contestNavElement.querySelectorAll('.cmp-contest-nav--logo').length
    ).to.equal(1);
  });

  it("should select and render the first filters option", function()  {
    expect(
      this.contestNavComponent.state.selectedOption
    ).to.equal(this.contestNavComponent.getSelectOptions()[0].option);

    if (this.contestNavComponent.state.selectedType == TYPE_SELECT_LINEUPS) {
      expect(
        this.contestNavElement.querySelectorAll('.cmp-contest-nav--lineups-list').length
      ).to.equal(1);
    } else if (this.contestNavComponent.state.selectedType == TYPE_SELECT_GAMES) {
      expect(
        this.contestNavElement.querySelectorAll('.cmp-contest-nav--games-list').length
      ).to.equal(1);
    } else {
      new Error("Selected contest-nav filter is not rendered.");
    }
  });

});
