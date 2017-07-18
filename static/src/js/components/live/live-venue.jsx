import React from 'react';
import LiveAnimationArea from './live-animation-area';
import LiveBigPlays from '../live/live-big-plays';
import LiveHeader from './live-header';
import LiveStandingsPane from './live-standings-pane';

export default React.createClass({
  propTypes: {
    bigPlaysQueue: React.PropTypes.array.isRequired,
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

    animationCompletedPromise.then(() => this.setState({ showPBPInfo: true }))
    // Wait for the description to be intro'd and displayed
    .then(() => wait(3000))
    // Clear the description
    .then(() => this.setState({ showPBPInfo: false, currentEvent: null }))
    // Wait for the stage and description to be removed
    .then(() => wait(1000))
    // Trigger onAnimationCompleted, if provided.
    .then(() => {
      if (this.props.onAnimationCompleted) {
        this.props.onAnimationCompleted();
      }
    });
  },

  render() {
    const { showPBPInfo, currentEvent } = this.state;
    const isLoadingContest = this.props.contest.isLoading;
    const isWatchingContest = this.props.watching.contestId !== null;

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

          <LiveAnimationArea
            watching={this.props.watching}
            currentEvent={currentEvent}
            eventsMultipart={this.props.eventsMultipart}
            onAnimationStarted={animationCompletedPromise => this.stageAnimationStarted(animationCompletedPromise)}
          />

          { isWatchingContest && !isLoadingContest &&
            <LiveStandingsPane contest={this.props.contest} watching={this.props.watching} />
          }
        </section>

        <LiveBigPlays queue={this.props.bigPlaysQueue} />
      </div>
    );
  },
});
