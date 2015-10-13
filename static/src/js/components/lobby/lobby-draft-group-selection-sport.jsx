'use strict';

var React = require('react');


/**
 * When choosing a draft group, the first step is to pick which sport you want, this renders
 * that list based off of sportContestCounts from the DraftGroupInfoStore.
 */
var LobbyDraftGroupSelectionSport = React.createClass({

  propTypes: {
    'sportContestCounts': React.PropTypes.object.isRequired,
    // When a sport is clicked, select the sport on the parent component.
    'onSportClick': React.PropTypes.func.isRequired
  },


  getDefaultProps: function() {
    return {
      sportContestCounts: {}
    };
  },


  render: function() {
    var sportList = [];

    for (var sport in this.props.sportContestCounts) {
      if (this.props.sportContestCounts.hasOwnProperty(sport)) {
        sportList.push(
          <li
            key={sport}
            className="cmp-draft-group-select__sport"
            onClick={this.props.onSportClick.bind(null, sport)}
          >
            <h4 className="cmp-draft-group-select__title">{sport}</h4>
            <div className="cmp-draft-group-select__sub">
              {this.props.sportContestCounts[sport]} contests
            </div>
          </li>
        );
      }
    }

    // If there are no active contests.
    if (!sportList.length) {
      return (
        <ul>
          <li>There are no active contests.</li>
        </ul>
      );
    }

    return (
      <ul>
        {sportList}
      </ul>
    );
  }
});


module.exports = LobbyDraftGroupSelectionSport;
