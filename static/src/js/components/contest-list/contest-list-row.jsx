import React from 'react';
import CountdownClock from '../site/countdown-clock.jsx';
import EnterContestButton from './enter-contest-button.jsx';
import uniq from 'lodash/uniq';
import ordinal from '../../lib/ordinal.js';
import { humanizeCurrency } from '../../lib/utils/currency.js';
import SportIcon from '../site/sport-icon.jsx';


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


  hasReachedMaxEntries(contest) {
    // Is our current entry count less than the contest's max entry value?
    if (contest.entryInfo) {
      return this.getEntryCount(contest) < contest.max_entries;
    }

    return false;
  },


  ignoreClick(e) {
    e.stopPropagation();
  },


  handleRowClick() {
    this.props.setFocusedContest(this.props.contest);
  },


  flash: '',


  renderPrizeRanks(prizeStructure) {
    let rankList = [];
    // Create an array of unique rank.value values. if there is only 1, then all
    // payouts are the same.
    const payoutIsFlat = uniq(prizeStructure.ranks.map(
        (rank) => rank.value)
      ).length === 1;

    if (prizeStructure.ranks) {
      if (payoutIsFlat && prizeStructure.ranks.length > 1) {
        rankList.push(
          <span key="h2h">
            1st - {ordinal(prizeStructure.ranks.length)}: {humanizeCurrency(prizeStructure.ranks[0].value)}
          </span>
        );
      } else {
        rankList = prizeStructure.ranks.map((rank, i, arr) => {
          const delimiter = i < arr.length - 1 ? '|' : '';
          return (
            <span key={i}>{ordinal(i + 1)}: {humanizeCurrency(rank.value)} {delimiter} </span>
          );
        });
      }
    }

    return rankList;
  },


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

    if (this.isAnotherLineupEntered(this.props.contest.entryInfo, this.props.focusedLineup)) {
      classes += ' other-lineup';
    }

    return (
      <tr
        onClick={this.handleRowClick}
        key={this.props.contest.id}
        className={classes}
      >
        <td key="sport" className="sport">
          <SportIcon sport={this.props.contest.sport} />
        </td>
        <td key="name" className="name">
          {this.props.contest.name}
        </td>
        <td key="payouts" className="payouts">
          {this.renderPrizeRanks(this.props.contest.prize_structure)}
        </td>
        <td key="entries" className="entries">{this.props.contest.current_entries}</td>
        <td key="contestSize" className="contest-size">{this.props.contest.contest_size}</td>
        <td key="start" className="start">
          <CountdownClock
            time={this.props.contest.start}
            timePassedDisplay="Live"
          />
        </td>

        <td key="user-entries" className="user-entries">
          {this.getEntryCount(this.props.contest)} of {this.props.contest.max_entries}
        </td>

        <td
          key="enter"
          className="enter"
          onClick={this.ignoreClick}
        >
          <EnterContestButton
            lineup={this.props.focusedLineup}
            contest={this.props.contest}
            lineupsInfo={this.props.lineupsInfo}
            onEnterClick={this.props.enterContest}
            onEnterSuccess={this.close}
            buttonClasses={{
              default: 'button--sm button--outline',
              contestEntered: 'button--sm button--flat',
              pending: 'button--sm button--flat',
              contestHasStarted: 'button--sm button--flat',
              maxEntered: 'button--sm button--flat',
            }}
          />
        </td>
      </tr>
    );
  },

});


module.exports = ContestListRow;
