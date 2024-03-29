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

const sortAsc = arr => arr.sort((a, b) => a.x - b.x);
const sortDesc = arr => arr.sort((a, b) => b.x - a.x);

const distributeRightToLeft = (lineups, minDist) => sortDesc(lineups).reduce((results, lineup) => {
  const curPos = lineup;
  if (results.length) {
    const prevPos = results[results.length - 1];
    const isOverlapping = (prevPos.x - curPos.x) < minDist;
    if (isOverlapping) {
      curPos.x = Math.max(0, Math.min(1, prevPos.x - minDist));
    }
  }
  return results.concat([curPos]);
}, []);

const distributeLeftToRight = (lineups, minDist) => sortAsc(lineups).reduce((results, lineup) => {
  const curPos = lineup;
  if (results.length) {
    const prevPos = results[results.length - 1];
    const isOverlapping = (curPos.x - prevPos.x) < minDist;
    if (isOverlapping) {
      curPos.x = Math.max(0, Math.min(1, prevPos.x + minDist));
    }
  }
  return results.concat([curPos]);
}, []);

const alignItems = (lineups, minDist) => {
  distributeRightToLeft(lineups, minDist);
  distributeLeftToRight(lineups, minDist);
  return lineups;
};

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
    }),
  },

  componentDidMount() {
    this.alignElements();
  },

  componentDidUpdate() {
    this.alignElements();
  },

  /**
   * Returns the loaded lineups as ranked lineups.
   */
  getRankedLineups() {
    const { contest } = this.props;

    if (contest.isLoading ||
      !contest.hasLineupsUsernames ||
      !contest.rankedLineups) {
      return [];
    }

    const prepareLineups = lineups => {
      const points = lineups.map(lineup => lineup.fp);
      const minFP = Math.min.apply(null, points);
      const maxFP = Math.max.apply(null, points);
      const range = maxFP - minFP;

      return lineups.map(lineup => (
        {
          id: lineup.id,
          fp: lineup.fp,
          username: contest.lineupsUsernames[lineup.id] || '',
          rank: lineup.rank,
          potentialWinnings: lineup.potentialWinnings,
          timeRemaining: lineup.timeRemaining.decimal,
          x: !range ? 0 : (lineup.fp - minFP) / range,
        }
      ));
    };

    // Ignore lineups that have an ID of "1". This is a hold over from previous
    // code that existed before our refactor. Maybe Craig knows?
    const lineups = contest.rankedLineups
    .filter(lineupId => lineupId !== 1)
    .map(lineupId => contest.lineups[lineupId])
    .sort((a, b) => b.rank - a.rank);

    return prepareLineups(lineups);
  },

  /**
   * Helper function for adjusting the position of "points" after the component
   * renders. This is to ensure the points can be accurately positioned based
   * on the drawn dimensions of the line.
   */
  alignElements() {
    const lineups = this.getRankedLineups();

    // When testing `requestAnimationFrame` is going to be undefined.
    if (!lineups.length || !window.requestAnimationFrame) {
      return null;
    }

    const standingsLineEl = this.refs.standingsline;
    const moneylineEl = this.refs.moneyline;
    const winners = lineups.filter(lineup => lineup.potentialWinnings > 0).sort(
      (a, b) => a.potentialWinnings - b.potentialWinnings
    );

    window.requestAnimationFrame(() => {
      // Get the width of the line to accurately determine the minimum space
      // between each absolutely positioned dot.
      const lineWidth = standingsLineEl.offsetWidth;
      const dotWidth = 15 / lineWidth;

      alignItems(lineups, dotWidth);

      const lastPosInTheMoney = winners.length ? winners[0].x : 0;

      lineups.forEach(lineup => {
        const lineupEl = this.refs[`lineup-${lineup.id}`];
        if (lineupEl) {
          lineupEl.style.left = `${lineup.x * 100}%`;
        }
      });

      moneylineEl.style.width = `${(1 - lastPosInTheMoney) * 100}%`;
    });
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
  renderMoneyLinePoint(lineup, watching) {
    const { id, fp, rank, timeRemaining, potentialWinnings, username } = lineup;
    const className = 'live-standings-pane__point';

    let classNames = className;
    let pmrColors = ['46495e', 'aab0be', 'aab0be'];

    // if my lineup
    if (watching.myLineupId === id) {
      pmrColors = ['46495e', '34B4CC', '2871AC'];
      classNames = `${classNames} ${className}--mine`;
    } else if (watching.opponentLineupId === id) {
      pmrColors = ['e33c3c', 'b52c4b', '871c5a'];
      classNames = `${classNames} ${className}--opponent`;
    } else if (potentialWinnings !== 0) {
      classNames = `${classNames} ${className}--winning`;
    } else {
      classNames = `${classNames} ${className}--losing`;
    }

    /* eslint-disable max-len */
    return (
      <div key={id} ref={`lineup-${id}`} className={classNames} onClick={this.handleViewOpponentLineup.bind(this, id)}>
        <div className="live-standings-pane__inner-point" />
        <div className="live-standing live-standings-pane__live-standing">
          <div className="live-standing__info">
            <div className="live-standing__place-and-earning">
              <div className="live-standing__place">{rank}</div>
              <div className="live-standing__earning">
                <div className="live-standing__earning-above">
                  {humanizeCurrency(+(potentialWinnings))}
                </div>
              </div>
            </div>
            <div className="live-standing__pmr">
              <LivePMRProgressBar colors={pmrColors} decimalRemaining={timeRemaining} svgWidth={50} id={`${id}Lineup`} />
            </div>
            <div className="live-standing__username">{username}</div>
            <div className="live-standing__fp">{humanizeFP(fp)} Pts</div>
          </div>
          {watching.myLineupId !== id &&
            <div className="live-standing__cta">CLICK TO COMPARE LINEUPS</div>
          }
        </div>
      </div>
    );
    /* eslint-enable max-len */
  },

  render() {
    const lineups = this.getRankedLineups();

    if (!lineups.length) {
      return null;
    }

    return (
      <div className="live-standings-pane">
        <div className="live-standings-pane__legend">1ST</div>
        <div ref="standingsline" className="live-standings-pane__lineups">
          <div ref="moneyline" className="live-standings-pane__moneyline" />
          {lineups.map(lineup =>
            this.renderMoneyLinePoint(lineup, this.props.watching)
          )}
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
