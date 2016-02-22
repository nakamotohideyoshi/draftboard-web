import React from 'react';
import CountdownClock from '../site/countdown-clock.jsx';
import EnterContestButton from './enter-contest-button.jsx';


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
    row: React.PropTypes.object.isRequired,
    columns: React.PropTypes.array,
    focusedLineup: React.PropTypes.object,
    focusedContest: React.PropTypes.object,
    highlighted: React.PropTypes.bool,
    enterContest: React.PropTypes.func,
    setFocusedContest: React.PropTypes.func,
    draftGroupsWithLineups: React.PropTypes.array,
    isEntered: React.PropTypes.bool,
    lineupsInfo: React.PropTypes.object,
  },


  componentWillReceiveProps(nextProps) {
    // Use this semi-janky method to run a css animation on an already-redered element.
    // https://github.com/ordishs/react-animation-example
    const newValue = nextProps.row.current_entries;

    if (this.props.row.current_entries !== newValue) {
      this.flash = this.flash === 'flash1' ? 'flash2' : 'flash1';
    }
  },


  ignoreClick(e) {
    e.stopPropagation();
  },


  handleRowClick() {
    this.props.setFocusedContest(this.props.row);
  },


  flash: '',


  render() {
    // If it's the currently focused contest, add a class to it.
    let classes = this.props.focusedContest.id === this.props.row.id ? 'active ' : '';
    classes += `cmp-contest-list__row ${this.flash}`;
    if (this.props.isEntered) {
      classes += ' entered';
    }

    if (this.props.highlighted) {
      classes += ' highlight';
    }

    // Icons
    let guaranteedIcon;
    if (this.props.row.gpp) {
      guaranteedIcon = <span className="contest-icon contest-icon__guaranteed">G</span>;
    }
    let multiEntryIcon;
    if (this.props.row.max_entries > 1) {
      multiEntryIcon = <span className="contest-icon contest-icon__multi-entry">M</span>;
    }


    return (
      <tr
        onClick={this.handleRowClick}
        key={this.props.row.id}
        className={classes}
      >
        <td key="sport" className="sport">
          <span className={`icon icon-${this.props.row.sport}`}></span>
        </td>
        <td key="name" className="name">{this.props.row.name} {guaranteedIcon}</td>
        <td key="entries" className="entries">
          {multiEntryIcon} {this.props.row.current_entries}/{this.props.row.entries}
        </td>
        <td key="fee" className="fee">${this.props.row.buyin}</td>
        <td key="prizes" className="prizes">${this.props.row.prize_pool}</td>
        <td key="start" className="start">
          <CountdownClock
            time={this.props.row.start}
            timePassedDisplay="Live"
          />
        </td>

        <td className="enter">
          <EnterContestButton
            lineup={this.props.focusedLineup}
            contest={this.props.row}
            lineupsInfo={this.props.lineupsInfo}
            onEnterClick={this.props.enterContest}
            onEnterSuccess={this.close}
          />

          <a
            className="button button--gradient--background draft-button"
            href={`/draft/${this.props.row.draft_group}/`}
            onClick={this.ignoreClick}
          >
            Draft
          </a>
        </td>
      </tr>
    );
  },

});


module.exports = ContestListRow;
