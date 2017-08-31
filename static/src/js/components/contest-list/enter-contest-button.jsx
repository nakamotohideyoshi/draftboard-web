import React from 'react';
import { isTimeInFuture } from '../../lib/utils.js';
import AppStateStore from '../../stores/app-state-store.js';
import Tooltip from '../site/tooltip.jsx';

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
    entrySkillLevels: React.PropTypes.object.isRequired,
  },


  getDefaultProps() {
    return {
      // button text for various states.
      buttonText: {
        draft: 'Draft',
        started: 'Contest Started',
        enter: 'Enter',
        entering: 'Entering...',
        entered: 'Enter Again',
        maxEntered: 'Max Entered',
      },
      buttonClasses: {
        default: 'button--sm button--outline',
        contestEntered: 'button--sm button--outline',
        pending: 'button--sm button--outline',
        contestHasStarted: 'button--sm button--outline',
        maxEntered: 'button--sm button--outline',
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


  /**
   * How many entries the user has in this contest pool.
   * @return {int} The number of entries.
   */
  getFocusedLineupEntryCount(contest) {
    if (contest.entryInfo) {
      return contest.entryInfo.length;
    }

    return 0;
  },


  /**
   * How many entries the user has in this contest pool.
   * @return {int} The number of entries.
   */
  getEntryCount(contest) {
    if (contest.entryInfo) {
      return contest.entryInfo.length;
    }

    return 0;
  },


  /**
   * Check if another lineup is already entered into this contest. If so, our currently focused lineup
   * cannot enter.
   * @param  {Array}  entryInfo     List of contest pool entries. this is nested in the contest prop.
   * @param  {Object}  focusedLineup The currently focused lineup.
   * @return {Boolean}
   */
  isAnotherLineupEntered(entryInfo, focusedLineup) {
    let enteredLineupId = null;

    if (entryInfo && entryInfo.length) {
      enteredLineupId = entryInfo[0].lineup;
    }

    if (enteredLineupId && focusedLineup) {
      return enteredLineupId !== focusedLineup.id;
    }

    return false;
  },


  ignoreClick(e) {
    e.stopPropagation();
  },


  matchesCurrentSkillLevel(contest) {
    // IF we have no entries at all, allow anything.
    if (!this.props.entrySkillLevels) {
      return true;
    }
    // If we have no current entries for this sport, allow entry.
    if (!this.props.entrySkillLevels[contest.sport]) {
      return true;
    }
    // If the contest allows any skill level to enter, allow entry.
    if (contest.skill_level.name === 'all') {
      return true;
    }
    // If we have a lineup entered into a contest, check for a match.
    return contest.skill_level.name === this.props.entrySkillLevels[contest.sport];
  },


  hasReachedMaxEntries(contest) {
    // Is our current entry count less than the contest's max entry value?
    if (contest.entryInfo) {
      return this.getFocusedLineupEntryCount(contest) < contest.max_entries;
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


    if (this.props.contest) {
      if (!this.matchesCurrentSkillLevel(this.props.contest)) {
        classes = this.props.buttonClasses.maxEntered;
        return (
          <div
            className={`button button--disabled ${classes} entered enter-contest-button`}
            onClick={this.ignoreClick}
            onMouseLeave={this.handleMouseOut}
          >
            Wrong Skill Level
            <Tooltip
              isVisible
              position={'bottom'}
            >
              <span>You may only enter into 1 skill level per sport.</span>
            </Tooltip>

          </div>
        );
      }
    }


    // This stuff can only apply if we know which lineup + contest we are dealing with.
    if (this.props.contest && this.props.lineup) {
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
            onMouseEnter={this.handleMouseOver}
            onMouseLeave={this.handleMouseOut}
          >
            {this.props.buttonText.entering}
          </div>
        );
      }


      // This contest pool has an entry in it...
      if (this.getEntryCount(this.props.contest) > 0) {
        classes = this.props.buttonClasses.contestEntered;

        // The contest has been entered the max number of times.
        if (!this.hasReachedMaxEntries(this.props.contest)) {
          classes = this.props.buttonClasses.maxEntered;

          return (
            <div
              className={`button button--disabled ${classes} entered enter-contest-button`}
              onClick={this.ignoreClick}
              onMouseLeave={this.handleMouseOut}
            >
              {this.props.buttonText.maxEntered}
            </div>
          );
        }


        // // Another lineup is already entered in the contest pool.
        // if (this.isAnotherLineupEntered(this.props.contest.entryInfo, this.props.lineup)) {
        //   return (
        //     <div
        //       className={`button ${classes} button--disabled has-tooltip entered enter-contest-button`}
        //       onClick={this.ignoreClick}
        //       onMouseLeave={this.handleMouseOut}
        //     >
        //       {this.props.buttonText.entered}
        //       <Tooltip
        //         isVisible
        //         position={'bottom'}
        //       >
        //         <span>You can only enter 1 lineup into a contest.</span>
        //       </Tooltip>
        //     </div>
        //   );
        // }

        // The focused contest already has an entry in it, and can add another.
        return (
          <div
            className={`button ${classes} entered enter-contest-button`}
            onClick={this.handleButtonClick.bind(null, this.props.contest)}
            onMouseEnter={this.handleMouseOver}
            onMouseLeave={this.handleMouseOut}
          >
            {this.props.buttonText.entered}
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
      <div className="enter-contest-button-none">&nbsp;</div>
    );
  },

});


module.exports = EnterContestButton;
