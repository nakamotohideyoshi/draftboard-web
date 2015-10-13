'use strict';

require("../../test-dom")();
var React = require('react');
var Component = require("../../../components/lobby/lobby-draft-group-selection-modal.jsx");
var expect = require('chai').expect;
var _ = require('lodash');
var DraftGroupsFixtures = require('../../../fixtures/draft-groups.js')[0].fixtures();

// Some default state + props.
var populatedState = {
  sportContestCounts: {'nba': 23, 'nhl': 4},
  draftGroups: DraftGroupsFixtures[0].results
};

var defaultProps = {};

// Render the component.
function render(newProps, callback) {
    var props = _.merge(defaultProps, newProps);
    var targetElement = document.body.appendChild(document.createElement('div'));
    return React.render(
      React.createElement(Component, props),
      targetElement, function() {
        if (typeof callback === 'function') setTimeout(callback);
    });
}


describe("LobbyDraftGroupSelectionModal Component", function() {

  afterEach(function() {
    document.body.innerHTML = '';
  });


  it("should show sport list when no sport is selected", function(done) {
    var _tree = render({}, function() {
      expect(document.querySelectorAll('.cmp-modal--draft-group-select').length).to.equal(1);

      // draft group selection should not be shown yet.
      expect(
        document.querySelectorAll('.cmp-draft-group-select__group').length
      ).to.equal(
        0
      );

      // when no sport is selected, the sports should be shown.
      _tree.setState({selectedSport: null, DraftGroupInfo: populatedState}, function() {
        expect(
          document.querySelectorAll('.cmp-draft-group-select__sport'
        ).length).to.equal(
          _.size(populatedState.sportContestCounts)
        );

        expect(
          document.querySelectorAll('.cmp-draft-group-select__sport').length
        ).to.be.at.least(1);

        done();
      });
    });
  });


  it("should render a list of draft groups list when a sport is selected", function(done) {
    var _tree = render({}, function() {
      expect(document.querySelectorAll('.cmp-modal--draft-group-select').length).to.equal(1);

      _tree.setState({selectedSport: 'nba', DraftGroupInfo: populatedState}, function() {
        // no sport selections.
        expect(document.querySelectorAll('.cmp-draft-group-select__sport').length).to.equal(0);
        // all draftgroup selections.
        expect(
          document.querySelectorAll('.cmp-draft-group-select__group').length
        ).to.equal(
          _.size(populatedState.draftGroups)
        );

        // there should be SOMETHING there. - this will fail if the fixtures get busted.
        expect(
          document.querySelectorAll('.cmp-draft-group-select__group').length
        ).to.be.at.least(1);

        done();
      });
    });
  });


});
