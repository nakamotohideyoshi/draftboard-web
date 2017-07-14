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
    animationCompleted: React.PropTypes.func.isRequired,
  },

  getInitialState() {
    return {
      completedEvent: null,
    };
  },

  stageAnimationCompleted(event) {
    // Trigger update to header... title & description
    this.setState({ completedEvent: event });
    setTimeout(() => {
      this.setState({ completedEvent: null });
      this.props.animationCompleted();
    }, 5000);
  },

  render() {
    const {
      completedEvent,
    } = this.state;

    const {
      contest,
      currentEvent,
      watching,
      myLineupInfo,
      uniqueLineups,
      opponentLineup,
      eventsMultipart,
      bigPlaysQueue,
    } = this.props;

    const isWatchingContest = watching.contestId !== null && !contest.isLoading;

    return (
      <div>
        <section className="live__venues">
          <LiveHeader
            contest={contest}
            watching={watching}
            lineups={uniqueLineups.lineups}
            myLineup={myLineupInfo}
            opponentLineup={opponentLineup}
            animationEvent={completedEvent}
          />

          <LiveAnimationArea
            watching={watching}
            currentEvent={currentEvent}
            eventsMultipart={eventsMultipart}
            onAnimationComplete={ (event) => this.stageAnimationCompleted(event) }
          />

          { isWatchingContest &&
            <LiveStandingsPane contest={contest} watching={watching} />
          }
        </section>

        <LiveBigPlays queue={bigPlaysQueue} />
      </div>
    );
  },
});
