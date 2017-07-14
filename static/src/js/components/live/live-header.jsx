import React from 'react';
import NFLPlayRecapVO from '../../lib/live-animations/nfl/NFLPlayRecapVO';
import { LiveOverallStatsConnected } from './live-overall-stats';

// assets
require('../../../sass/blocks/live/live-header.scss');

export default React.createClass({

  propTypes: {
    animationEvent: React.PropTypes.object,
    contest: React.PropTypes.object.isRequired,
    myLineup: React.PropTypes.object.isRequired,
    lineups: React.PropTypes.array.isRequired,
    opponentLineup: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  /**
   * Renders the DOM for displaying the current animation event's information.
   */
  renderAnimationInfo() {
    if (!this.props.animationEvent) {
      return null;
    }

    const playVO = new NFLPlayRecapVO(this.props.animationEvent);

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
    const modifiers = !this.props.animationEvent ? [] : ['event-ended'];

    // If the lineups name is falsy just show the lineup owner's username.
    let name;
    try {
      name = lineup.name || this.props.contest.lineupsUsernames[lineup.id];
    } catch (e) {
      name = '';
    }

    return (
      <LiveOverallStatsConnected
        id={lineup.id}
        fp={lineup.fp}
        lineups={this.props.lineups}
        name={name}
        modifiers={modifiers}
        potentialWinnings={potentialWinnings}
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
