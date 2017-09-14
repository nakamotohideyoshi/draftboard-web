import React from 'react';
import { LiveOverallStatsConnected } from './live-overall-stats';

// assets
require('../../../sass/blocks/live/live-header.scss');

export default React.createClass({

  propTypes: {
    title: React.PropTypes.object,
    contest: React.PropTypes.object.isRequired,
    myLineup: React.PropTypes.object.isRequired,
    lineups: React.PropTypes.array.isRequired,
    opponentLineup: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
    message: React.PropTypes.shape({
      title: React.PropTypes.string,
      description: React.PropTypes.string,
    }),
  },

  /**
   * Renders the DOM for displaying the current animation event's information.
   */
  renderAnimationInfo() {
    if (!this.props.message) {
      return null;
    }

    return (
      <div className="live-header__animation-info live-header__animation-info--show">
        { this.props.message.title &&
          <h2 className="live-header__animation-info__type">
            {`${this.props.message.title.toUpperCase()}`}
          </h2>
        }
        { this.props.message.description &&
          <div className="live-header__animation-info__description">
            {this.props.message.description}
          </div>
        }
      </div>
    );
  },

  /**
   * Renders a LiveOverallStatsConnected component.
   */
  renderOverallStats(whichSide, lineup, contest = null) {
    const modifiers = !this.props.message ? [] : ['event-ended'];

    // If the lineups name is falsy just show the lineup owner's username.
    let name;
    try {
      name = lineup.name || contest.lineupsUsernames[lineup.id];
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
        potentialWinnings={lineup.potentialWinnings}
        rank={lineup.rank}
        timeRemaining={lineup.timeRemaining}
        whichSide={whichSide}
        watching={this.props.watching}
      />
    );
  },

  render() {
    const { myLineup, contest, opponentLineup, watching } = this.props;

    if (myLineup.isLoading) {
      return null;
    }

    const hasContest = watching.contestId && contest && !contest.isLoading;
    const hasOpponentLineup = watching.opponentLineupId && !opponentLineup.isLoading;
    const myCurrentLineup = hasContest ? contest.lineups[myLineup.id] : myLineup;

    return (
      <header className="live-header">
        <h2 className="live-header__contest-name">{contest.name || '  '}</h2>
        {this.renderOverallStats('mine', myCurrentLineup, contest)}
        {hasContest && hasOpponentLineup && (
          this.renderOverallStats('opponent', opponentLineup, contest)
        )}
        {this.renderAnimationInfo()}
      </header>
    );
  },
});
