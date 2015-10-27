'use strict';

require('../../test-dom')();
var React = require('react');
var ReactDOM = require('react-dom');
var LiveNBACourt = require('../../../components/live-nba/live-nba-court.jsx');
var expect = require('chai').expect;
var request = require("superagent");
var config = require('../../../fixtures/live-nba-store-config.js');
var log = require("../../../lib/logging");


// need to repeat the component with different data, so sadly can't use a beforeEach method
describe('LiveNBACourt Component', function() {

  before(function(done) {
    var self = this;
    this.timeout(10000);

    this.superagentMock = require('superagent-mock')(request, config);
    this.LiveNBAStore = require('../../../stores/live-nba-store');

    // replace log method to listen and check messages
    var prev = log.debug;

    log.debug = function (arg) {
      if (self.LiveNBAStore.data.initLoaded === true) {
        // restore logging
        log.debug = prev;

        done();
      }
    };

    var LiveNBAActions = require('../../../actions/live-nba-actions');

    LiveNBAActions.loadContestLineups(1);
    LiveNBAActions.loadDraftGroup(1);
    LiveNBAActions.loadDraftGroupFantasyPoints(1);
    LiveNBAActions.loadLineup(2, 'mine');
    LiveNBAActions.loadLineup(3, 'opponent');
  });


  after(function() {
    this.superagentMock.unset();

    // reset data
    this.LiveNBAStore.resetData();
  });


  it('should render a <section>', function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = ReactDOM.render(
      <LiveNBACourt />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var courtElement = ReactDOM.findDOMNode(this);
        expect(courtElement.tagName).to.equal('SECTION');
      }
    );
  });


  it("should not render shooters with no history events", function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = ReactDOM.render(
      <LiveNBACourt />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var courtElement = ReactDOM.findDOMNode(this);
        expect(courtElement.querySelectorAll('.shooter-position').length).to.equal(0);
      }
    );
  });


  it("should render shooters when history event is pushed", function(done) {
    this.timeout(6000);
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = ReactDOM.render(
      <LiveNBACourt />,
      document.body.appendChild(document.createElement('div')),
      function() {

        self.LiveNBAStore._onEventReceived({
          "game__id": "a0f4ab88-e622-4041-8f9d-f3c6b954ed43",
          "id": "825e52a1-a6b1-49e2-8aad-269522a63bcf",
          "location__list": {
            "coord_x": 119,
            "coord_y": 26
          },
          "statistics__list": {
            "assist__list": {
              "player": "5e5099d1-4a58-43f2-8d03-f2ae5dd49337",
              "team": "583ec825-fb46-11e1-82cb-f4ce4684ea4c"
            },
            "fieldgoal__list": {
              "made": "true",
              "player": "79d56fd7-f4ed-4905-9d04-dff4b5352334",
              "points": 3,
              "shot_type": "jump shot",
              "team": "583ec825-fb46-11e1-82cb-f4ce4684ea4c",
              "three_point_shot": "true"
            }
          }
        });

        var courtElement = ReactDOM.findDOMNode(this);

        setTimeout(function () {
          expect(courtElement.querySelectorAll('.shooter-position').length).to.be.above(0);

          // now wait until court animation is done
          setTimeout(function() {
            done();
          }, 3000);
        }, 2000);

      }
    );
  });

});
