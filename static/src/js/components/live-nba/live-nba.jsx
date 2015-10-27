'use strict';

var React = require('react');
var Reflux = require('reflux');
var renderComponent = require('../../lib/render-component');
var LiveNBAActions = require("../../actions/live-nba-actions");
var LiveNBALineup = require('./live-nba-lineup');
var LiveNBACourt = require('./live-nba-court');
var LiveNBAStore = require("../../stores/live-nba-store");
var LiveNBAOverallStats = require('./live-nba-overall-stats');


/**
 * The overarching component for the live NBA section.
 *
 * Connects with the LiveNBAStore for data.
 * This will be where the state changes and then properties are cascaded down to the other child components.
 */
var LiveNBA = React.createClass({
  mixins: [
    Reflux.connect(LiveNBAStore)
  ],

  // Load in the players, their fantasy points, and my lineup
  getInitialState: function() {
    LiveNBAActions.loadContestLineups(1);
    LiveNBAActions.loadDraftGroup(1);
    LiveNBAActions.loadDraftGroupFantasyPoints(1);
    LiveNBAActions.loadLineup(3, 'mine');
    LiveNBAActions.loadLineup(4, 'opponent');
  },

  render: function() {
    return (
      <div>

        <LiveNBALineup whichSide="me" />

        <section className="live-nba__court-scoreboard">
          <header className="live-nba__scoreboard live-scoreboard">
            <h1 className="live-scoreboard__contest-name">$150K NBA Championship</h1>
            <LiveNBAOverallStats whichSide="me" />

          </header>

          <LiveNBACourt />

          <section className="live-winning-graph">
            <div className="live-winning-graph__pmr-line">
              <span style={{ width: '79%'}}></span>
            </div>

            <h3 className="live-winning-graph__limits live-winning-graph__min">$0</h3>
            <h2 className="live-winning-graph__earnings">$8,221</h2>
            <h3 className="live-winning-graph__limits live-winning-graph__max">$10,000</h3>
          </section>

        </section>

        <LiveNBALineup whichSide="opponent" />
      </div>
    );
  }

});


renderComponent(<LiveNBA />, '.live-nba');


module.exports = LiveNBA;
