import React from 'react';
import LineupCardEntry from './lineup-card-entry.jsx';
import forEach from 'lodash/forEach';


const LineupCardEntries = React.createClass({

  propTypes: {
    lineupInfo: React.PropTypes.object.isRequired,
    flipCard: React.PropTypes.func.isRequired,
  },

  getEntries() {
    const entries = [];

    forEach(this.props.lineupInfo.contestPoolEntries, (entry) => {
      entries.push(<LineupCardEntry key={entry.contest.id} entry={entry} />);
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
