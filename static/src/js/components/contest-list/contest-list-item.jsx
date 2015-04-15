"use strict";

var React = require("react");
var ContestActions = require("../../actions/contest-actions");

var ContestListItem = React.createClass({

  setContestFocus: function(e) {
    ContestActions.contestFocused(this.props.contest.id);
  },

  render: function() {
    return (
      <tr onClick={this.setContestFocus}>
      <td>{this.props.contest.title}</td>
      <td>{this.props.contest.entries_filled}/{this.props.contest.entries_total}</td>
      <td>{this.props.contest.prize}</td>
      </tr>
    );
  }

});


module.exports = ContestListItem;
