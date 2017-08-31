import * as ReactRedux from 'react-redux';
import React from 'react';
import { addOrdinal } from '../../lib/utils/numbers';
import LivePMRProgressBar from './live-pmr-progress-bar';
import { bindActionCreators } from 'redux';
import { humanizeCurrency } from '../../lib/utils/currency';
import { humanizeFP } from '../../lib/utils/numbers';
import { updateLiveMode, updateWatchingAndPath } from '../../actions/watching.js';

// assets
require('../../../sass/blocks/live/live-standings-pane.scss');
require('../../../sass/blocks/live/live-standing.scss');

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component, wrapped in 'action' key
 */
const mapDispatchToProps = (dispatch) => ({
  actions: bindActionCreators({
    updateLiveMode,
    updateWatchingAndPath,
  }, dispatch),
});

/**
 * When `View Contests` element is clicked, open side pane to show
 * a user's current contests for that lineup.
 */
export const LiveStandingsPane = React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
    contest: React.PropTypes.shape({
      lineups: React.PropTypes.object,
      hasLineupsUsernames: React.PropTypes.bool,
      lineupsUsernames: React.PropTypes.object,
      rankedLineups: React.PropTypes.array,
      prize: React.PropTypes.shape({
        info: React.PropTypes.shape({
          payout_spots: React.PropTypes.number,
        }),
      }),
    }),
  },

  /**
   * Returns the username for the lineup if it exists.
   */
  getUsernameForLineup(lineupId) {
    return this.props.contest.lineupsUsernames[lineupId] || '';
  },

  /**
   * Returns the cross section of lineups that exist in both the `props.lineups`
   * and in `props.rankedLineups`.
   */
  getRankedLineups() {
    return this.props.contest.rankedLineups
    .filter(lineupId =>
      // Ignore lineups that have an ID of "1". This is a hold over from previous
      // code that Justen didn't know why existed, but did exist, so he did not
      // want to remove it during his refactor. Maybe Craig knows?
      lineupId !== 1
    )
    .map(lineupId => this.props.contest.lineups[lineupId])
    .sort((a, b) => b.fp - a.fp);
  },

  /**
   * Returns an array of positions based on the provided array of lineups.
   */
  getRankedLineupPositions(lineups) {
    const points = lineups.map((lineup) => lineup.fp);
    const minFP = Math.min.apply(null, points);
    const maxFP = Math.max.apply(null, points);
    const range = maxFP - minFP;

    return lineups.map(lineup =>
      ((lineup.fp - minFP) / range) * 100
    );
  },

  /**
   * Used to view an opponent lineup. Sets up parameters to then call props.updateWatchingAndPath()
   */
  handleViewOpponentLineup(opponentLineupId) {
    const { actions, watching } = this.props;

    // can't watch yousrelf!
    if (opponentLineupId === watching.myLineupId) return false;

    const lineupUrl = `/live/${watching.sport}/lineups/${watching.myLineupId}`;
    const path = `${lineupUrl}/contests/${watching.contestId}/opponents/${opponentLineupId}/`;
    const changedFields = {
      opponentLineupId,
    };

    actions.updateWatchingAndPath(path, changedFields);
  },

  /**
   * Renders the div for a single lineup.
   */
  renderMoneyLinePoint(lineup, placement) {
    const watching = this.props.watching;
    const decimalRemaining = lineup.timeRemaining.decimal;
    const className = 'live-standings-pane__point';
    const potentialWinnings = lineup.potentialWinnings;

    let classNames = className;
    let pmrColors = ['46495e', 'aab0be', 'aab0be'];

    // if my lineup
    if (watching.myLineupId === lineup.id) {
      pmrColors = ['46495e', '34B4CC', '2871AC'];
      classNames = `${classNames} ${className}--mine`;
    } else if (watching.opponentLineupId === lineup.id) {
      pmrColors = ['e33c3c', 'b52c4b', '871c5a'];
      classNames = `${classNames} ${className}--opponent`;
    } else if (potentialWinnings !== 0) {
      classNames = `${classNames} ${className}--winning`;
    } else {
      classNames = `${classNames} ${className}--losing`;
    }

    return (
      <div
        key={lineup.id}
        className={classNames}
        onClick={this.handleViewOpponentLineup.bind(this, lineup.id)}
        style={{ left: `${placement}%` }}
      >
        <div className="live-standings-pane__inner-point" />

        <div className="live-standing live-standings-pane__live-standing">
          <div className="live-standing__info">
            <div className="live-standing__place-and-earning">
              <div className="live-standing__place">{lineup.rank}</div>
              <div className="live-standing__earning">
                <div className="live-standing__earning-above">
                  {humanizeCurrency(+(potentialWinnings))}
                </div>
              </div>
            </div>
            <div className="live-standing__pmr">
              <LivePMRProgressBar
                colors={pmrColors}
                decimalRemaining={decimalRemaining}
                svgWidth={50}
                id={`${lineup.id}Lineup`}
              />
            </div>
            <div className="live-standing__username">{this.getUsernameForLineup(lineup.id)}</div>
            <div className="live-standing__fp">{humanizeFP(lineup.fp)} Pts</div>
          </div>
          {watching.myLineupId !== lineup.id &&
            <div className="live-standing__cta">CLICK TO COMPARE LINEUPS</div>
          }
        </div>
      </div>
    );
  },

  render() {
    const { contest } = this.props;

    if (contest.isLoading ||
      !contest.hasLineupsUsernames ||
      !contest.rankedLineups ||
      contest.rankedLineups.length <= 2) {
      return null;
    }

    const numWinners = contest.prize.info.payout_spots;
    const lineups = this.getRankedLineups();
    const positions = this.getRankedLineupPositions(lineups);
    const lastPosInTheMoney = positions[Math.min(numWinners, positions.length) - 1];
    const moneyLineWidth = 100 - lastPosInTheMoney;
    const moneyLinePoints = lineups.map((lineup, index) =>
      this.renderMoneyLinePoint(lineup, positions[index])
    );

    return (
      <div className="live-standings-pane">
        <div className="live-standings-pane__legend">1ST</div>
        <div className="live-standings-pane__lineups">
          <div className="live-standings-pane__moneyline" style={{ width: `${moneyLineWidth}%` }} />
          {moneyLinePoints}
        </div>
        <div className="live-standings-pane__legend">{addOrdinal(lineups.length)}</div>
      </div>
    );
  },
});

// Redux integration
const { connect } = ReactRedux;

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  () => ({}),
  mapDispatchToProps
)(LiveStandingsPane);
