"use strict";

var React = require("react");
var Reflux = require("reflux");
var renderComponent = require('../../lib/render-component');
var ContestStore = require("../../stores/contest-store.js");
var ReactAddons = require('react/addons');
var ReactCSSTransitionGroup = ReactAddons.addons.CSSTransitionGroup;
var AppActions = require('../../actions/app-actions');
var KeypressActions = require('../../actions/keypress-actions');


var ContestListDetail = React.createClass({
  mixins: [
    // ContestStore,
    Reflux.ListenerMixin
  ],

  getInitialState: function() {
    return {
      focusedContest: ContestStore.getFocusedContest()
    };
  },

  onContestsChange: function() {
    // Since the store changed, grab the newest focused contest.
    this.setState({
      focusedContest: ContestStore.getFocusedContest()
    });
  },

  componentDidMount: function() {
    // When the contest store changes, run onContestsChange.
    this.listenTo(ContestStore, this.onContestsChange);

    KeypressActions.keypressESC.listen(function() {
      AppActions.closePane();
    });
  },

  render: function() {
    // Default state.
    var contest = <div>Select a contest</div>;

    // Show focused contest info, if there is one.
    if (typeof (this.state.focusedContest) !== "undefined" && this.state.focusedContest !== null) {

      contest = (
        <ReactCSSTransitionGroup transitionName="example">
          <div key={this.state.focusedContest.id} className="cmp-contest-detail--contest">

            <header className="cmp-contest-detail--header">
              <div className="cmp-contest-detail--entries">{this.state.focusedContest.entries_filled}/{this.state.focusedContest.entries_total}</div>
              <h4 className="cmp-contest-detail--title">{this.state.focusedContest.title}</h4>

              <ul className="cmp-contest-detail--details">
                <li><span className="title">Fee</span> $xx</li>
                <li><span className="title">Prize Pool</span> {this.state.focusedContest.prize}</li>
                <li><span className="title">Live In</span> {this.state.focusedContest.startTime}</li>
              </ul>
            </header>

          </div>
        </ReactCSSTransitionGroup>
      );
    }

    return (contest);
  }

});



// Render the component.
renderComponent(<ContestListDetail />, '.cmp-contest-detail');

module.export = ContestListDetail;
