import React from 'react';
import { humanizeCurrency } from '../../lib/utils/currency';
import { generateBlockNameWithModifiers } from '../../lib/utils/bem';

// assets
require('../../../sass/blocks/live/live-contests-pane-item.scss');


/**
 * A single item in the list of contests on LiveContestPane
 */
const LiveContestsPaneItem = React.createClass({

  propTypes: {
    backToContestsPane: React.PropTypes.func.isRequired,
    contest: React.PropTypes.object.isRequired,
    contestsSize: React.PropTypes.number.isRequired,
    index: React.PropTypes.number.isRequired,
    onItemClick: React.PropTypes.func.isRequired,
    modifiers: React.PropTypes.array.isRequired,
  },

  /**
   * Propogating up a click handler to choose this contest to view
   */
  _onClick() {
    this.props.onItemClick(this.props.contest.id);
  },

  render() {
    const { contest, modifiers, contestsSize } = this.props;
    const block = 'live-contests-pane-item';
    const classNames = generateBlockNameWithModifiers(block, modifiers);
    const winnings = contest.potentialWinnings;
    let earnings = (<div className={`${block}__has-earnings`}></div>);

    let { index } = this.props;
    if (index.toString().length === 1) index = `0${index}`;

    // if user is making money, show them how much
    if (winnings > 0) {
      earnings = (
        <div className={`${block}__has-earnings`}>
          &nbsp;-&nbsp;<div className={`${block}__earnings`}>{humanizeCurrency(winnings)}</div>
        </div>
      );
    }

    let backToContestsDom;
    if (contestsSize > 1 && modifiers.indexOf('active') > -1) {
      backToContestsDom = (
        <div className={`${block}__back-to-contests`} onClick={this.props.backToContestsPane}>
          <svg viewBox="0 0 16 16" className={`${block}__close-contest`}>
            <line x1="0" y1="0" x2="16" y2="16" />
            <line x1="0" y1="16" x2="16" y2="0" />
          </svg>
        </div>
      );
    }

    return (
      <li className={classNames}>
        <div className={`${block}__view`} onClick={this._onClick}>
          <div className={`${block}__divider`} />
          <div className={`${block}__rank`}>{index}</div>
          <div className={`${block}__name`}>{contest.name}</div>
          <div className={`${block}__place`}>{contest.myEntryRank} of {contest.entriesCount}</div>
          {earnings}
        </div>
        {backToContestsDom}
      </li>
    );
  },
});

export default LiveContestsPaneItem;
