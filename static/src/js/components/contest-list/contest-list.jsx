"use strict";

var React = require("react");
var ContestStore = require("../../stores/contest-store");
var ContestListItem = require("./contest-list-item.jsx");


var ContestTable = React.createClass({
  mixins: [
    //Reflux.connect(ContestStore, "contestData")
  ],

  getInitialState: function() {
    return {contests: ContestStore.getAllContests()};
  },

  onChange: function(contestData) {
    this.setState({
      contests: contestData.contests
    });
  },

  componentDidMount: function() {
    this.unsubscribe = ContestStore.listen(this.onChange);
  },

  componentWillUnmount: function() {
    this.unsubscribe();
  },

  sortTableByKey: function(key) {
    ContestStore.sortByKey(key);
  },

  render: function () {
    var contests = this.state.contests || [];

    var contestListItems = contests.map(function(contest) {
      return (
        <ContestListItem key={contest.id} contest={contest} />
      );
    });

    return (
      <table>
        <tbody>
          <tr>
            <th onClick={this.sortTableByKey.bind(this, "title")}>Title</th>
            <th onClick={this.sortTableByKey.bind(this, "entries_total")}>Entries</th>
            <th onClick={this.sortTableByKey.bind(this, "prize")}>Prize</th>
          </tr>
          {contestListItems}
        </tbody>
      </table>
    );
  }

});



module.exports = ContestTable;
