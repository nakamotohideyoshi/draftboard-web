import React from 'react';
import NBAPlayRecapVO from '../../lib/live-animations/nba/NBAPlayRecapVO';
import { LiveOverallStatsConnected } from './live-overall-stats';

// assets
require('../../../sass/blocks/live/live-header.scss');

export default React.createClass({

  propTypes: {
    currentEvent: React.PropTypes.object,
    contest: React.PropTypes.object.isRequired,
    myLineup: React.PropTypes.object.isRequired,
    lineups: React.PropTypes.array.isRequired,
    opponentLineup: React.PropTypes.object.isRequired,
    selectLineup: React.PropTypes.func.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  /**
   * Renders the DOM for displaying the current animation event's information.
   */
  renderAnimationInfo() {
    if (!this.props.currentEvent) {
      return null;
    }

    const playVO = new NBAPlayRecapVO(this.props.currentEvent);

    return (
      <div className="live-header__animation-info live-header__animation-info--show">
        <h2 className="live-header__animation-info__type">
          {`${playVO.playTitle().toUpperCase()}`}
        </h2>
        <div className="live-header__animation-info__description">
          {playVO.playDescription()}
        </div>
      </div>
    );
  },

  /**
   * Renders a LiveOverallStatsConnected component.
   */
  renderOverallStats(whichSide, lineup, potentialWinnings, rank) {
    const modifiers = !this.props.currentEvent ? [] : ['event-ended'];

    return (
      <LiveOverallStatsConnected
        id={lineup.id}
        fp={lineup.fp}
        lineups={this.props.lineups}
        name={lineup.name}
        modifiers={modifiers}
        potentialWinnings={potentialWinnings}
        selectLineup={this.props.selectLineup}
        rank={rank}
        timeRemaining={lineup.timeRemaining}
        whichSide={whichSide}
        watching={this.props.watching}
      />
    );
  },

  render() {
    const { myLineup, contest, opponentLineup, watching } = this.props;
    const isWatchingContest = watching.contestId !== null && contest.isLoading === false;
    const showOpponentLineup = watching.opponentLineupId !== null && opponentLineup.isLoading === false;

    let { potentialWinnings, rank } = myLineup;

    if (myLineup.isLoading !== false) {
      return null;
    }

    // if watching a contest, then update the titles and ensure the overall stats are contest-based.
    if (isWatchingContest) {
      potentialWinnings = contest.potentialWinnings;
      rank = contest.rank;
    }

    return (
      <header className="live-header">
        <h2 className="live-header__contest-name">{contest.name || '  '}</h2>
        {this.renderOverallStats('mine', myLineup, potentialWinnings, rank)}
        {isWatchingContest && showOpponentLineup &&
          this.renderOverallStats('opponent', opponentLineup, potentialWinnings, rank)
        }
        {this.renderAnimationInfo()}
      </header>
    );
  },
});
