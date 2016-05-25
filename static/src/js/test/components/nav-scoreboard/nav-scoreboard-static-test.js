'use strict';

require('../../test-dom')();
const React = require('react');
const ReactDOM = require('react-dom');
import NavScoreboardStatic from '../../../components/nav-scoreboard/nav-scoreboard-static.jsx';
const expect = require('chai').expect;

const {TYPE_SELECT_GAMES, TYPE_SELECT_LINEUPS} = NavScoreboardStatic;

describe("NavScoreboardStatic Component", function() {

  beforeEach(function(done) {
    window.dfs.user = {
      username: 'test'
    };

    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.component = ReactDOM.render(
      React.createElement(NavScoreboardStatic, {
        user: {username: 'fasfas'},
        sportsSelector: {
          types: ['type1'],
          type1: {
            gameIds: [1],
          },
          games: {
            1: {
              awayTeamInfo: {alias: '1'},
              homeTeamInfo: {alias: '2'},
            }
          }
        },
        myCurrentLineupsSelector: {},
        cashBalance: '132123',
        isLivePage: 'faf',
      }),
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.element = ReactDOM.findDOMNode(this);
        done();
      }
    );
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  it('should render a div tag, menu, user info, filters, slider and logo', function() {
    expect(this.element.tagName).to.equal('DIV');
    expect(
      this.element.querySelectorAll('.cmp-nav-scoreboard--menu').length
    ).to.equal(1);
    expect(
      this.element.querySelectorAll('.cmp-nav-scoreboard--user-info').length
    ).to.equal(1);
    expect(
      this.element.querySelectorAll('.cmp-nav-scoreboard--filters').length
    ).to.equal(1);
    expect(
      this.element.querySelectorAll('.cmp-nav-scoreboard--slider').length
    ).to.equal(1);
    expect(
      this.element.querySelectorAll('.cmp-nav-scoreboard--logo').length
    ).to.equal(1);
  });

  it("should select and render the first filters option", function()  {
    expect(
      this.component.state.selectedOption
    ).to.equal(this.component.getSelectOptions()[0].option);

    if (this.component.state.selectedType == TYPE_SELECT_LINEUPS) {
      expect(
        this.element.querySelectorAll('.cmp-nav-scoreboard--lineups-list').length
      ).to.equal(1);
    } else if (this.component.state.selectedType == TYPE_SELECT_GAMES) {
      expect(
        this.element.querySelectorAll('.cmp-nav-scoreboard--games-list').length
      ).to.equal(1);
    } else {
      new Error("Selected nav-scoreboard filter is not rendered.");
    }
  });

});
