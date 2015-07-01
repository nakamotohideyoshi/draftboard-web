"use strict";

var React = require("react");
var ContestActions = require("../../actions/contest-actions");
var AppActions = require("../../actions/app-actions");

var ContestListItem = React.createClass({

  propTypes: {
    contest: React.PropTypes.object
  },

  setContestFocus: function(e) {
    e.preventDefault();
    ContestActions.contestFocused(this.props.contest.id);
    AppActions.somethingOn();
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
