import React from 'react';


/**
 * A single item in the list of contests on LiveContestPane
 */
const LiveContestsPaneItem = React.createClass({

  propTypes: {
    contest: React.PropTypes.object.isRequired,
    onItemClick: React.PropTypes.func.isRequired,
  },

  /**
   * Propogating up a click handler to choose this contest to view
   */
  _onClick() {
    this.props.onItemClick(this.props.contest.id);
  },

  render() {
    const contest = this.props.contest;
    let moneyLineClass = 'live-moneyline';

    if (contest.percentageCanWin <= contest.myPercentagePosition) {
      moneyLineClass += ' live-moneyline--is-losing';
    }

    let winnings = contest.potentialEarnings;
    let winningsClass = 'winnings';
    if (winnings === 0) {
      winnings = `$${winnings}`;
    } else {
      winnings = `$${winnings.toFixed(2)}`;
      winningsClass += ' active';
    }

    // flip to be to the right
    const myPercentagePosition = 100 - contest.myPercentagePosition;

    return (
      <li className="live-contests-pane__contest" key={ contest.id }>
        <div className="live-contests-pane__name">{ contest.name }</div>
        <div className="live-contests-pane__place">
          <span className="live-contests-pane__place--mine">{ contest.myEntryRank }</span> of { contest.entriesCount }
        </div>
        <div className="live-contests-pane__stats">
          <span className="fees">${ contest.buyin }</span>
          {" "} / {" "}
          <span className={winningsClass}>{ winnings }</span>
        </div>

        <section className={ moneyLineClass }>
          <div className="live-moneyline__pmr-line">
            <div className="live-moneyline__winners" style={{ width: `${contest.percentageCanWin}%` }}></div>
            <div
              className="live-moneyline__current-position"
              style={{ left: `${myPercentagePosition}%` }}
            ></div>
          </div>
        </section>

        <div className="live-contest-cta" onClick={this._onClick}>View contest</div>
      </li>
    );
  },
});

export default LiveContestsPaneItem;
