import React from 'react';
import { isTimeInFuture } from '../../lib/utils.js';


/**
 * A time-aware button that takes you to a draft page for the provided draft group.
 * It will automatically disable itself once the disableTime has passed.
 */
const DraftButton = React.createClass({

  propTypes: {
    draftGroupId: React.PropTypes.number.isRequired,
    disableTime: React.PropTypes.string.isRequired,
  },


  getInitialState() {
    return {
      hasContestStarted: false,
    };
  },

  componentWillMount() {
    const self = this;
    // Start a loop that will keep checking if the contest has started yet.
    this.checkStartStatusLoop = window.setInterval(self.checkStartStatus, 2000);
    this.checkStartStatus();
  },


  componentWillUnmount() {
    window.clearInterval(this.checkStartStatusLoop);
  },

  ignoreClick(e) {
    e.stopPropagation();
  },

  // This gets continuously looped to determine if the contest has started.
  checkStartStatus() {
    const contestHasStarted = !isTimeInFuture(this.props.disableTime);
    // Only update the state (and thus re-render) if something has changed.
    if (contestHasStarted !== this.state.hasContestStarted) {
      this.setState({
        hasContestStarted: contestHasStarted,
      });
    }
  },


  render() {
    // If the window to enter the contest has passed, do not show a button.
    if (this.state.hasContestStarted) {
      return (
        <span className="draft-button draft-button-none"></span>
      );
    }

    return (
      <a
        className="button button--sm button--outline-alt1 draft-button"
        href={`/draft/${this.props.draftGroupId}/`}
        onClick={this.ignoreClick}
      >
        Draft
      </a>
    );
  },

});


module.exports = DraftButton;
