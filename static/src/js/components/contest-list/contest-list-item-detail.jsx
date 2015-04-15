"use strict";

var React = require("react");
var Reflux = require("reflux");
var ContestStore = require("../../stores/contest-store");


var ContestListItemDetail = React.createClass({
  mixins: [ContestStore, Reflux.ListenerMixin],

  getInitialState: function() {
    return {};
  },

  getDefaultProps: function() {
    return {
      focusedContest: ContestStore.getFocusedContest()
    };
  },

  onContestsChange: function() {
    // Since the store changed, grab the newest focused contest.
    this.setProps({focusedContest: ContestStore.getFocusedContest()});
  },

  componentDidMount: function() {
    // When the contest store changes, run onContestsChange.
    this.listenTo(ContestStore, this.onContestsChange);
  },

  render: function() {
    // Default state;
    var contest = <div>Select a contest</div>;

    // Show focused contest info, if there is one.
    if (typeof (this.props.focusedContest) !== "undefined" && this.props.focusedContest !== null) {
      contest = (
        <div>
          <h5>Selected Contest</h5>
          <h4>{this.props.focusedContest.title}</h4>
          <h5>Details:</h5>
          <div>{this.props.focusedContest.entries_filled}/{this.props.focusedContest.entries_total}</div>
          <div>{this.props.focusedContest.prize}</div>
        </div>
      );
    }

    return (contest);
  }

});


React.render(<ContestListItemDetail />, document.getElementById("contest-detail"));

module.export = ContestListItemDetail;
