import React from 'react';
import find from 'lodash/find';


/**
 * A single entry row in the list on the back of a lineup card.
 */
const LineupCardContestEntrySet = React.createClass({
  propTypes: {
    entrySet: React.PropTypes.object.isRequired,
    removeContestPoolEntry: React.PropTypes.func.isRequired,
    unregisterRequests: React.PropTypes.object.isRequired,
  },


  getEntryIds(entries) {
    return entries.map((entry) => entry.id);
  },

  handleOnClick() {
    if (this.props.entrySet.entries) {
      this.props.removeContestPoolEntry(this.props.entrySet.entries[0]);
    }
  },

  isUnregistering(entryIds, unregisterRequests) {
    return find(unregisterRequests, (request) => entryIds.indexOf(request.entryId) > -1) !== undefined;
  },


  renderRemoveButton() {
    const unregistering = this.isUnregistering(
      this.getEntryIds(this.props.entrySet.entries),
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
        <span className="contest">{this.props.entrySet.contest.name}</span>
        <span className="fees">
          ${this.props.entrySet.contest.buyin.toLocaleString('en')} x {this.props.entrySet.entryCount}
        </span>
      </li>
    );
  },
});


module.exports = LineupCardContestEntrySet;
