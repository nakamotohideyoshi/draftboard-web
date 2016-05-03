import React from 'react';
import log from '../../lib/logging.js';
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
    buttonClasses: React.PropTypes.object,
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
      buttonClasses: {
        default: 'button--sm button--outline',
        contestEntered: 'button--sm button--outline',
        pending: 'button--sm button--outline',
        contestHasStarted: 'button--sm button--outline',
      },
    };
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
      if (props.lineupsInfo.hasOwnProperty(props.lineup.id) && props.lineupsInfo[props.lineup.id].entryRequests) {
        return props.lineupsInfo[props.lineup.id].entryRequests[props.contest.id];
      }
    } else {
      return null;
    }
  },


  ignoreClick(e) {
    e.stopPropagation();
  },


  canLineupEnterContestPool(lineup, lineupsInfo, contest) {
    let entryCount = 0;

    try {
      entryCount = lineupsInfo[lineup.id].contestPoolEntries[contest.id].entryCount;
    } catch (e) {
      // Ignore any Type Errors from the above not being populated yet.
      if (e instanceof TypeError) {
        log.trace(e);
      } else {
        throw e;
      }
    }


    return entryCount < contest.max_entries;
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

    const contestHasStarted = !isTimeInFuture(this.props.contest.start);
    // Only update the state (and thus re-render) if something has changed.
    if (contestHasStarted !== this.state.hasContestStarted) {
      this.setState({
        hasContestStarted: contestHasStarted,
      });
    }
  },


  render() {
    const currentEntryRequest = this.getCurrentEntryRequest(this.props);

    let classes = '';

    // If the window to enter the contest has passed, disable the button.
    if (this.state.hasContestStarted) {
      classes = this.props.buttonClasses.contestHasStarted;

      return (
        <span
          className={`button ${classes} button--disabled enter-contest-button`}
          onClick={this.ignoreClick}
        >
          {this.props.buttonText.started}
        </span>
      );
    }


    // This stuff can only apply if we know which lineup + contest we are dealing with.
    if (this.props.contest && this.props.lineup) {
      // The contest has been entered the max number of times.
      if (!this.canLineupEnterContestPool(this.props.lineup, this.props.lineupsInfo, this.props.contest)) {
        classes = this.props.buttonClasses.contestEntered;

        return (
          <div
            className={`button button--disabled ${classes} entered enter-contest-button`}
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
        classes = this.props.buttonClasses.pending;

        return (
          <div
            className={`button ${classes} button--working enter-contest-button`}
            onClick={this.ignoreClick}
          >
            {this.props.buttonText.entering}
          </div>
        );
      }

      // If there is no pending entry request, but the lineup can be entered, show the enter
      // contest button.
      if (this.props.lineup.draft_group === this.props.contest.draft_group) {
        classes = this.props.buttonClasses.default;

        return (
          <div
            className={`button ${classes} enter-contest-button`}
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
