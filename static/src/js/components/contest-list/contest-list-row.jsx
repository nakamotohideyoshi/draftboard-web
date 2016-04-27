import React from 'react';
import CountdownClock from '../site/countdown-clock.jsx';
import EnterContestButton from './enter-contest-button.jsx';
import DraftButton from './draft-button.jsx';


/**
 * Render a single ContestList 'row'.
 * contest list specific functionality.
 *
 * Clicking the row sets it as the active contest in the Store.
 *
 * @param {Object} row - A single row of the DataTable's data.
 * @param {array} columns - The columns that should be displayed. This is directly passed down
 * through DataTable.
 */
const ContestListRow = React.createClass({


  propTypes: {
    draftGroupsWithLineups: React.PropTypes.array,
    enterContest: React.PropTypes.func,
    focusedContest: React.PropTypes.object,
    focusedLineup: React.PropTypes.object,
    highlighted: React.PropTypes.bool,
    isEntered: React.PropTypes.bool,
    lineupsInfo: React.PropTypes.object,
    contest: React.PropTypes.object.isRequired,
    setFocusedContest: React.PropTypes.func,
  },


  componentWillReceiveProps(nextProps) {
    // Use this semi-janky method to run a css animation on an already-redered element.
    // https://github.com/ordishs/react-animation-example
    const newValue = nextProps.contest.current_entries;

    if (this.props.contest.current_entries !== newValue) {
      this.flash = this.flash === 'flash1' ? 'flash2' : 'flash1';
    }
  },


  getLineupEntryCount(focusedLineup) {
    if (focusedLineup &&
        this.props.contest &&
        this.props.lineupsInfo.hasOwnProperty(focusedLineup.id) &&
        this.props.lineupsInfo[focusedLineup.id].contestPoolEntries.hasOwnProperty(this.props.contest.id)
      ) {
      return this.props.lineupsInfo[focusedLineup.id].contestPoolEntries[this.props.contest.id].entryCount;
    }
    return 0;
  },


  ignoreClick(e) {
    e.stopPropagation();
  },


  handleRowClick() {
    this.props.setFocusedContest(this.props.contest);
  },


  flash: '',


  render() {
    // If it's the currently focused contest, add a class to it.
    let classes = this.props.focusedContest.id === this.props.contest.id ? 'active ' : '';
    classes += `cmp-contest-list__row ${this.flash}`;
    if (this.props.isEntered) {
      classes += ' entered';
    }

    if (this.props.highlighted) {
      classes += ' highlight';
    }

    // Icons
    let guaranteedIcon;
    if (this.props.contest.gpp) {
      guaranteedIcon = <span className="contest-icon contest-icon__guaranteed">G</span>;
    }
    let multiEntryIcon;
    if (this.props.contest.max_entries > 1) {
      multiEntryIcon = <span className="contest-icon contest-icon__multi-entry">M</span>;
    }


    return (
      <tr
        onClick={this.handleRowClick}
        key={this.props.contest.id}
        className={classes}
      >
        <td key="sport" className="sport">
          <span className={`icon icon-${this.props.contest.sport}`}></span>
        </td>
        <td key="name" className="name">
          {this.props.contest.name} {this.props.contest.sport} CONTEST POOLS HAVE NO NAMES! {guaranteedIcon}
        </td>
        <td key="entries" className="entries">
          {multiEntryIcon} {this.props.contest.current_entries}/∞
        </td>
        <td key="fee" className="fee">${this.props.contest.buyin}</td>
        <td key="prizes" className="prizes">${this.props.contest.prize_pool}</td>
        <td key="start" className="start">
          <CountdownClock
            time={this.props.contest.start}
            timePassedDisplay="Live"
          />
        </td>

        <td className="user-entries">
          {this.getLineupEntryCount(this.props.focusedLineup)} of {this.props.contest.max_entries}
        </td>

        <td className="enter">
          <DraftButton
            draftGroupId={this.props.contest.draft_group}
            disableTime={this.props.contest.start}
          />

          <EnterContestButton
            lineup={this.props.focusedLineup}
            contest={this.props.contest}
            lineupsInfo={this.props.lineupsInfo}
            onEnterClick={this.props.enterContest}
            onEnterSuccess={this.close}
          />
        </td>
      </tr>
    );
  },

});


module.exports = ContestListRow;
