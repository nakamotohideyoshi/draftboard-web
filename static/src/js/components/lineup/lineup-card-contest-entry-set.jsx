import React from 'react';
import find from 'lodash/find';


/**
 * A single entry row in the list on the back of a lineup card.
 */
const LineupCardContestEntrySet = React.createClass({
  propTypes: {
    entry: React.PropTypes.object.isRequired,
    entrySet: React.PropTypes.object.isRequired,
    removeContestPoolEntry: React.PropTypes.func.isRequired,
    unregisterRequests: React.PropTypes.object.isRequired,
    entryIndex: React.PropTypes.number.isRequired,
  },


  handleOnClick() {
    if (this.props.entrySet.entries) {
      this.props.removeContestPoolEntry(this.props.entry);
    }
  },

  isUnregistering(entryId, unregisterRequests) {
    return find(unregisterRequests, (request) => entryId === request.entryId) !== undefined;
  },


  formatTitle() {
    if (this.props.entryIndex > 0) {
      return `${this.props.entrySet.contest.name} #${this.props.entryIndex + 1}`;
    }

    return this.props.entrySet.contest.name;
  },


  renderRemoveButton() {
    const unregistering = this.isUnregistering(
      this.props.entry.id,
      this.props.unregisterRequests
    );

    // If there is an outstanding unregistration request - show a 'working'
    // spinner image.
    if (unregistering) {
      return (
        <span className="remove-button button-working"></span>
      );
    }

    // Othewise show the default [x] button.
    return (
      <span
        onClick={this.handleOnClick}
        className="remove-button button-remove"
      >
      </span>
    );
  },


  render() {
    return (
      <li className="entry">
        <span className="remove">
          <div className="button-container">{this.renderRemoveButton()}</div>
        </span>
        <span className="contest">{this.formatTitle()}</span>
        <span className="fees">
          ${this.props.entrySet.contest.buyin.toLocaleString('en')}
        </span>
      </li>
    );
  },
});


module.exports = LineupCardContestEntrySet;
