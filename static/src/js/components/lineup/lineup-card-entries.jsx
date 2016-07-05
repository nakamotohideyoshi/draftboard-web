import React from 'react';
import LineupCardContestEntrySet from './lineup-card-contest-entry-set.jsx';
import forEach from 'lodash/forEach';


/**
 * Renders a list of a user's contest pool entries for use on the back of
 * a lineup card.
 */
const LineupCardEntries = React.createClass({

  propTypes: {
    lineupInfo: React.PropTypes.object.isRequired,
    flipCard: React.PropTypes.func.isRequired,
    removeContestPoolEntry: React.PropTypes.func.isRequired,
    draftGroupInfo: React.PropTypes.object.isRequired,
  },

  getEntries() {
    const entries = [];

    forEach(this.props.lineupInfo.contestPoolEntries, (entrySet) => {
      entrySet.entries.map((entry, i) => {
        entries.push(
          <LineupCardContestEntrySet
            key={`${entrySet.contest.id}-${i}`}
            entrySet={entrySet}
            entry={entry}
            unregisterRequests={this.props.lineupInfo.unregisterRequests}
            removeContestPoolEntry={this.props.removeContestPoolEntry}
            entryIndex={i}
          />
        );
      });
    });

    return entries;
  },


  render() {
    return (
      <div className="cmp-lineup-card-entries">
        <ul className="entry-list">
          {this.getEntries()}
        </ul>
      </div>
    );
  },
});


module.exports = LineupCardEntries;
