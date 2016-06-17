import React from 'react';
import LobbyDraftGroupSelectionSportItem from './lobby-draft-group-selection-sport-item.jsx';
import LobbyDraftGroupSelectionTime from './lobby-draft-group-selection-time.jsx';

/**
 * When choosing a draft group, the first step is to pick which sport you want, this renders
 * that list based off of sportContestCounts from the DraftGroupInfoStore.
 */
const LobbyDraftGroupSelectionSport = React.createClass({

  propTypes: {
    draftGroupInfo: React.PropTypes.object.isRequired,
    // When a sport is clicked, select the sport on the parent component.
    onSportClick: React.PropTypes.func.isRequired,
  },


  getDefaultProps() {
    return {
      sportContestCounts: {},
    };
  },


  render() {
    const { sportContestCounts, sportDraftGroupCounts } = this.props.draftGroupInfo;
    const sportList = [];

    for (const sport in sportContestCounts) {
      // If the sport only has 1 draft group. Show that rather than the sport.
      if (sportDraftGroupCounts[sport] && sportDraftGroupCounts[sport] === 1) {
        sportList.push(
          <LobbyDraftGroupSelectionTime
            key={sport}
            draftGroups={this.props.draftGroupInfo.draftGroups}
            selectedSport={sport}
          />
        );
      } else {
        // The sport has more than 1 draft group, so we show the sport which will
        // then display it's draft groups when selected.
        sportList.push(
          <LobbyDraftGroupSelectionSportItem
            key={sport}
            sportContestCounts={sportContestCounts}
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
