import * as ReactRedux from 'react-redux';
import map from 'lodash/map';
import React from 'react';
import { addOrdinal, iterativeRelaxation } from '../../lib/utils/numbers';
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
    hasLineupsUsernames: React.PropTypes.bool.isRequired,
    lineups: React.PropTypes.object.isRequired,
    lineupsUsernames: React.PropTypes.object.isRequired,
    rankedLineups: React.PropTypes.array.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  /**
   * Get list data that should be rendered in the current tab.
   * @return {Array}
   */
  getListData() {
    const { lineups, rankedLineups } = this.props;

    return map(rankedLineups, (lineupId) => lineups[lineupId]);
  },

  /**
   * Used to view an opponent lineup. Sets up parameters to then call props.updateWatchingAndPath()
   */
  handleViewOpponentLineup(opponentLineupId) {
    const { actions, watching } = this.props;

    // can't watch youself!
    if (opponentLineupId === watching.myLineupId) return false;

    const lineupUrl = `/live/${watching.sport}/lineups/${watching.myLineupId}`;
    const path = `${lineupUrl}/contests/${watching.contestId}/opponents/${opponentLineupId}/`;
    const changedFields = {
      opponentLineupId,
    };

    actions.updateWatchingAndPath(path, changedFields);
  },

  renderStandings() {
    const { lineupsUsernames } = this.props;
    const data = this.getListData();
    const watching = this.props.watching;

    const points = data.map((lineup) => lineup.fp);
    const lastPlacePoints = Math.max.apply(null, points);
    const firstPlacePoints = Math.min.apply(null, points);
    let range = firstPlacePoints - lastPlacePoints;

    if (range === 0) range = 1;

    const placements = iterativeRelaxation(data.map((lineup) => (lineup.fp - lastPlacePoints) / range * 100));

    let index = 0;
    const standings = data.filter((lineup) => lineup.id !== 1).map((lineup) => {
      const decimalRemaining = lineup.timeRemaining.decimal;
      const className = 'live-standings-pane__point';
      let classNames = className;
      const username = lineupsUsernames[lineup.id] || '';
      const potentialWinnings = lineup.potentialWinnings;
      const liveStandingName = 'live-standing';

      let cta = (<div className={`${liveStandingName}__cta`}>CLICK TO COMPARE LINEUPS</div>);

      let pmr = (
        <LivePMRProgressBar
          colors={['46495e', 'aab0be', 'aab0be']}
          decimalRemaining={decimalRemaining}
          svgWidth={50}
          id={`${lineup.id}Lineup`}
        />
      );

      // if my lineup
      if (watching.myLineupId === lineup.id) {
        classNames = `${classNames} ${className}--mine`;
        cta = null;

        pmr = (
          <LivePMRProgressBar
            colors={['46495e', '34B4CC', '2871AC']}
            decimalRemaining={decimalRemaining}
            svgWidth={50}
            id={`${lineup.id}Lineup`}
          />
        );
      } else if (potentialWinnings !== 0) {
        classNames = `${classNames} ${className}--winning`;
      } else {
        classNames = `${classNames} ${className}--losing`;
      }

      const leftPercent = `${placements[index]}%`;

      index++;

      return (
        <div
          key={lineup.id}
          className={classNames}
          onClick={this.handleViewOpponentLineup.bind(this, lineup.id)}
          style={{ left: leftPercent }}
        >
          <div className="live-standings-pane__inner-point" />

          <div className={`${liveStandingName} live-standings-pane__live-standing`}>
            <div className={`${liveStandingName}__info`}>
              <div className={`${liveStandingName}__place-and-earning`}>
                <div className={`${liveStandingName}__place`}>{lineup.rank}</div>
                <div className={`${liveStandingName}__earning`}>
                  <div className={`${liveStandingName}__earning-above`}>
                    {humanizeCurrency(+(potentialWinnings))}
                  </div>
                </div>
              </div>
              <div className={`${liveStandingName}__pmr`}>{pmr}</div>
              <div className={`${liveStandingName}__username`}>{username}</div>
              <div className={`${liveStandingName}__fp`}>{humanizeFP(lineup.fp)} Pts</div>
            </div>
            {cta}
          </div>
        </div>
      );
    });

    return standings;
  },

  render() {
    // wait for usernames
    if (this.props.hasLineupsUsernames === false) return null;

    const block = 'live-standings-pane';
    const lastPlace = addOrdinal(this.props.rankedLineups.length);

    return (
      <div className={block}>
        <div className={`${block}__legend ${block}__legend--first`}>1ST</div>
        <div className={`${block}__legend ${block}__legend--last`}>{lastPlace}</div>
        <div className="live-standings-pane__in-the-money" />
        {this.renderStandings()}
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
