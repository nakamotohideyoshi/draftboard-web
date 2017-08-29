import React from 'react';
import LiveMLBStage from './live-stage-mlb';
import LiveHistoryList from '../live/live-history-list';
import LiveHeader from './live-header';
import LiveStage from './live-stage';
import LiveStandingsPane from './live-standings-pane';

export default React.createClass({
  propTypes: {
    eventsMultipart: React.PropTypes.object,
    contest: React.PropTypes.object.isRequired,
    currentEvent: React.PropTypes.object,
    myLineupInfo: React.PropTypes.object.isRequired,
    opponentLineup: React.PropTypes.object.isRequired,
    uniqueLineups: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
    onAnimationCompleted: React.PropTypes.func,
  },

  getInitialState() {
    return {
      showPBPInfo: false,
      currentEvent: this.props.currentEvent || null,
    };
  },

  componentWillReceiveProps(nextProps) {
    this.setState({ currentEvent: nextProps.currentEvent });
  },

  stageAnimationStarted(animationCompletedPromise) {
    // Helper method for delaying callbacks within a promise chain.
    const wait = time => new Promise(resolve => setTimeout(resolve, time));

    animationCompletedPromise.then(() => this.setState({ showPBPInfo: false }))
    // Wait for the description to be intro'd and displayed
    // .then(() => wait(3000))
    // Clear the description
    .then(() => this.setState({ showPBPInfo: false, currentEvent: null }))
    // Wait for the stage and description to be removed
    .then(() => wait(1000))
    // Trigger onAnimationCompleted, if provided.
    .then(() => (
      this.props.onAnimationCompleted ? this.props.onAnimationCompleted() : true
    ));
  },

  render() {
    const { showPBPInfo, currentEvent } = this.state;
    const isLoadingContest = this.props.contest.isLoading;
    const isWatchingContest = this.props.watching.contestId !== null;
    const isWatchingMLB = this.props.watching.sport === 'mlb';

    return (
      <div>
        <section className="live__venues">
          <LiveHeader
            contest={this.props.contest}
            watching={this.props.watching}
            lineups={this.props.uniqueLineups.lineups}
            myLineup={this.props.myLineupInfo}
            opponentLineup={this.props.opponentLineup}
            animationEvent={showPBPInfo ? currentEvent : null}
          />

          {isWatchingMLB ? (
            <LiveMLBStage
              watching={this.props.watching}
              currentEvent={currentEvent}
              eventsMultipart={this.props.eventsMultipart}
              onAnimationStarted={animationCompletedPromise => this.stageAnimationStarted(animationCompletedPromise)}
            />
          ) : (
            <LiveStage
              key={`${this.props.watching.sport}-stage`}
              sport={this.props.watching.sport}
              currentEvent={this.props.currentEvent}
              onAnimationStarted={(p) => this.stageAnimationStarted(p)}
            />
          )}

          { isWatchingContest && !isLoadingContest &&
            <LiveStandingsPane contest={this.props.contest} watching={this.props.watching} />
          }
        </section>

        <LiveHistoryList currentEvent={this.props.currentEvent} />
      </div>
    );
  },
});
