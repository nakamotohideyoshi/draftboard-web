import React from 'react';
import { isTimeInFuture } from '../../lib/utils.js';
import AppStateStore from '../../stores/app-state-store.js';

/**
 * This is a button that allows the user to enter a contest and shows the status of an entry.
 * It is used in the lobby on each contest list row, the confirm entry modal, and the contest
 * detail sidebar.
 *
 * It will change states based on the status of pending entry requests, current contest entries,
 * contest availabilty, and the enter-ability of a lineup into a contest.
 */
const EnterContestButton = React.createClass({

  propTypes: {
    contest: React.PropTypes.object.isRequired,
    lineup: React.PropTypes.object,
    lineupsInfo: React.PropTypes.object.isRequired,
    onEnterClick: React.PropTypes.func,
    onEnterSuccess: React.PropTypes.func,
    onEnterFail: React.PropTypes.func,
    buttonText: React.PropTypes.object,
  },


  getDefaultProps() {
    return {
      // button text for various states.
      buttonText: {
        draft: 'Draft',
        started: 'Contest Started',
        enter: 'Enter',
        entering: 'Entering...',
        entered: 'Entered',
      },
    };
  },


  getInitialState() {
    return {
      hasContestStarted: false,
    };
  },


  componentWillMount() {
    // Start a loop that will keep checking if the contest has started yet.
    this.checkStartStatusLoop = window.setInterval(self.checkStartStatus, 1000);
  },


  // If the parent component tells us the modal should be closed via prop change, close it.
  // The parent can also call this components 'close()' method directly.
  componentWillReceiveProps(nextProps) {
    // If we recieve a 'success' status for the entry request, close the modal.
    const currentEntryStatus = this.getCurrentEntryRequest(nextProps);
    if (currentEntryStatus) {
      // Do any callback functions we've been passed (to close a modal or whatever).
      if (currentEntryStatus.status === 'SUCCESS') {
        if (this.props.onEnterSuccess) {
          this.props.onEnterSuccess();
        }
      }
    }
  },


  componentWillUnmount() {
    window.clearInterval(this.checkStartStatusLoop);
  },


  // Based on the focused lineup + contest, get an EntryRequest (if any).
  getCurrentEntryRequest(props) {
    if (!props) {
      return null;
    }

    if (
      props.lineup &&
      props.contest &&
      props.contest.hasOwnProperty('id')
    ) {
      if (props.lineupsInfo[props.lineup.id].entryRequests) {
        return props.lineupsInfo[props.lineup.id].entryRequests[props.contest.id];
      }
    } else {
      return null;
    }
  },


  ignoreClick(e) {
    e.stopPropagation();
  },


  isLineupEnteredIntoContest() {
    const entryRequest = this.getCurrentEntryRequest();
    if (entryRequest && entryRequest.status === 'SUCCESS') {
      return true;
    }
    if (this.props.lineup && this.props.lineupsInfo[this.props.lineup.id].contests) {
      // If we have an entry for the contest in our lineupsInfo selector.
      if (this.props.lineupsInfo[this.props.lineup.id].contests.indexOf(this.props.contest.id) !== -1) {
        return true;
      }
    }

    return false;
  },


  handleMouseOver() {
    AppStateStore.enterContestButtonMouseOver();
  },


  handleMouseOut() {
    AppStateStore.enterContestButtonMouseOut();
  },


  handleButtonClick(contest, e) {
    e.stopPropagation();
    this.props.onEnterClick(contest);
  },


  // This gets continuously looped to determine if the contest has started.
  checkStartStatus() {
    if (!this.props.contest) {
      return;
    }

    this.setState({
      hasContestStarted: !isTimeInFuture(this.props.contest.start),
    });
  },


  render() {
    const currentEntryRequest = this.getCurrentEntryRequest(this.props);

    // If the window to enter the contest has passed, disable the button.
    if (this.state.hasContestStarted) {
      return (
        <span
          className={"button button--mini--outline button--green-outline"}
          onClick={this.ignoreClick}
        >
          {this.props.buttonText.started}
        </span>
      );
    }


    // This stuff can only apply if we know which lineup + contest we are dealing with.
    if (this.props.contest && this.props.lineup) {
      // The contest has been entered.
      if (this.isLineupEnteredIntoContest()) {
        return (
          <div
            className="button disabled enter-contest-button entered"
            onClick={this.ignoreClick}
          >
            {this.props.buttonText.entered}
          </div>
        );
      }

      // If we have a pending entry request, don't do anything onClick.
      if (currentEntryRequest &&
        currentEntryRequest.status !== 'FAILURE' &&
        currentEntryRequest.status !== 'POLLING_TIMEOUT'
      ) {
        return (
          <div
            className="button button--gradient--background disabled enter-contest-button"
            onClick={this.ignoreClick}
          >
            {this.props.buttonText.entering}
          </div>
        );
      }

      // If there is no pending entry request, but the lineup can be entered, show the enter
      // contest button.
      if (this.props.lineup.draft_group === this.props.contest.draft_group) {
        return (
          <div
            className="button button--gradient--background enter-contest-button"
            onClick={this.handleButtonClick.bind(null, this.props.contest)}
            onMouseEnter={this.handleMouseOver}
            onMouseLeave={this.handleMouseOut}
          >
            {this.props.buttonText.enter}
          </div>
        );
      }
    }

    return (
      <div className="enter-contest-button-none"></div>
    );
  },

});


module.exports = EnterContestButton;
