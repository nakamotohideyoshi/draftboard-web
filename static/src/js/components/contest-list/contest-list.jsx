"use strict";

var React = require("react");
var Reflux = require("reflux");
var ContestStore = require("../../stores/contest-store");
var ContestListItem = require("./contest-list-item.jsx");


var ContestTable = React.createClass({
  mixins: [
    Reflux.connect(ContestStore, "contestData")
  ],

  getInitialState: function() {
    return {};
  },

  render: function () {
    var contestListItems = this.state.contestData.contests.map(function(contest) {
      return (
        <ContestListItem key={contest.id} contest={contest} />
      );
    });

    return (
      <table>
        <tr>
          <th>Title</th>
          <th>Entries</th>
          <th>Prize</th>
        </tr>
        {contestListItems}
      </table>
    );
  }

});


React.render(<ContestTable />, document.getElementById("contest-table"));

module.exports = ContestTable;
