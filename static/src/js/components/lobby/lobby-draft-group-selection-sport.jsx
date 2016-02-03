import React from 'react';
import LobbyDraftGroupSelectionSportItem from './lobby-draft-group-selection-sport-item.jsx';


/**
 * When choosing a draft group, the first step is to pick which sport you want, this renders
 * that list based off of sportContestCounts from the DraftGroupInfoStore.
 */
const LobbyDraftGroupSelectionSport = React.createClass({

  propTypes: {
    sportContestCounts: React.PropTypes.object.isRequired,
    // When a sport is clicked, select the sport on the parent component.
    onSportClick: React.PropTypes.func.isRequired,
  },


  getDefaultProps() {
    return {
      sportContestCounts: {},
    };
  },


  render() {
    const sportList = [];

    for (const sport in this.props.sportContestCounts) {
      if (this.props.sportContestCounts.hasOwnProperty(sport)) {
        sportList.push(
          <LobbyDraftGroupSelectionSportItem
            key={sport}
            sportContestCounts={this.props.sportContestCounts}
            sport={sport}
            onItemClick={this.props.onSportClick}
          />
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
  },

});


module.exports = LobbyDraftGroupSelectionSport;
