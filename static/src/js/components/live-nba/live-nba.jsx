'use strict';

var React = require('react');
var Reflux = require('reflux');
var renderComponent = require('../../lib/render-component');
var LiveNBALineup = require('./live-nba-lineup');
var LiveNBAHistory = require('./live-nba-history');
var LiveNBACourt = require('./live-nba-court');
var LiveNBAStore = require("../../stores/live-nba-store");


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

  render: function() {
    return (
      <div>
        <LiveNBALineup whichSide="me" />

        <section className="live-nba__court-scoreboard">
          <header className="live-nba__scoreboard live-scoreboard">
            <h1 className="live-scoreboard__contest-name">$150K NBA Championship</h1>

            <section className="live-winning-graph">
              <div className="live-winning-graph__pmr-line">
                <span style={{ width: '79%'}}></span>
              </div>

              <h3 className="live-winning-graph__limits live-winning-graph__min">$0</h3>
              <h2 className="live-winning-graph__earnings">$8,221</h2>
              <h3 className="live-winning-graph__limits live-winning-graph__max">$10,000</h3>
            </section>

            <section className="live-overview live-overview--lineup">
              <div className="live-overview__contests">
                <div className="live-overview__help">
                  Contests
                </div>
                <h4 className="live-overview__quantity">8</h4>
              </div>

              <div className="live-overview__points">
                <div className="live-overview__help">
                  Points
                </div>
                <h4 className="live-overview__quantity">123</h4>
              </div>

              <div className="live-overview__entries">
                <div className="live-overview__help">
                  Entries
                </div>
                <h4 className="live-overview__quantity">63</h4>
              </div>

              <section className="live-stack-choice live-stack-choice--me">
                <div className="live-stack-choice__title">
                  <span>◆</span> Warriors Stack
                </div>
              </section>

              <section className="live-stack-choice live-stack-choice--opponent">
                <div className="live-stack-choice__title">
                  <span>◆</span> Ppgogo
                </div>
              </section>
            </section>

          </header>

          <LiveNBACourt />
        </section>

        <LiveNBALineup whichSide="opponent" />

        <LiveNBAHistory whichSide='me' data={ LiveNBAStore.data.myHistoryEvents } />

        <LiveNBAHistory whichSide='opponent' data={ LiveNBAStore.data.opponentHistoryEvents } />
      </div>
    );
  }

});


renderComponent(<LiveNBA />, '.live-nba');


module.exports = LiveNBA;
