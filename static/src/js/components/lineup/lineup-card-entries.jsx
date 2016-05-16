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
  },

  getEntries() {
    const entries = [];

    forEach(this.props.lineupInfo.contestPoolEntries, (entrySet) => {
      entries.push(
        <LineupCardContestEntrySet
          key={entrySet.contest.id}
          entrySet={entrySet}
          unregisterRequests={this.props.lineupInfo.unregisterRequests}
          removeContestPoolEntry={this.props.removeContestPoolEntry}
        />
      );
    });

    return entries;
  },


  render() {
    return (
      <div className="cmp-lineup-card-entries">
        <header className="cmp-lineup-card__header">
          <h3 className="cmp-lineup-card__title">
            {this.props.lineupInfo.name || `Untitled Lineup # ${this.props.lineupInfo.id}`}
          </h3>

          <div className="actions-menu-container">
            <ul className="actions">
              <li>
                <div
                  className="icon-flop action"
                  onClick={this.props.flipCard}
                ></div>
              </li>
            </ul>
          </div>
        </header>

        <ul className="entry-list">
          {this.getEntries()}
        </ul>
      </div>
    );
  },
});


module.exports = LineupCardEntries;
