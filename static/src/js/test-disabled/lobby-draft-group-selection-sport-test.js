'use strict';

require("../../test-dom")();
var React = require("react");
var MyComponent = require("../../../components/lobby/lobby-draft-group-selection-sport.jsx");
var expect = require('chai').expect;

var defaultProps = {
  sportContestCounts: {'nba': 23, 'nhl': 4, 'nfl': 44},
  onSportClick: function() {}
};


describe("LobbyDraftGroupSelectionSport Component", function() {

  beforeEach(function() {
    this.targetElement = document.body.appendChild(document.createElement('div'));
  });


  afterEach(function() {
    document.body.innerHTML = '';
  });


  it("should always render a UL", function() {
    React.render(
      <MyComponent
        sportContestCounts={defaultProps.sportContestCounts}
        onSportClick={defaultProps.onSportClick}
      />,
      this.targetElement,
      function() {
        expect(this.getDOMNode().tagName).to.equal('UL');
      }
    );
  });


  it("should have an LI for each sport", function() {
    React.render(
      <MyComponent
        sportContestCounts={defaultProps.sportContestCounts}
        onSportClick={defaultProps.onSportClick}
      />,
      this.targetElement,
      function() {
        expect(this.getDOMNode().querySelectorAll('li').length).to.equal(3);
      }
    );
  });


  it("should render a single LI when there are no sports", function() {
    var noSports = {};

    React.render(
      <MyComponent
        sportContestCounts={noSports}
        onSportClick={defaultProps.onSportClick}
      />,
      this.targetElement,
      function() {
        expect(this.getDOMNode().querySelectorAll('li').length).to.equal(1);
      }
    );
  });

});
