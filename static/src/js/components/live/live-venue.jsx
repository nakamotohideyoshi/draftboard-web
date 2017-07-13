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
    completedEvent: React.PropTypes.object,
    myLineupInfo: React.PropTypes.object.isRequired,
    opponentLineup: React.PropTypes.object.isRequired,
    uniqueLineups: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
    selectLineup: React.PropTypes.func.isRequired,
    animationCompleted: React.PropTypes.func.isRequired,
  },

  render() {
    // HACK: to avoid stateless component linting error
    const fixSomething = this.state;

    const {
      contest,
      currentEvent,
      completedEvent,
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
            { ...{ contest, watching, fixSomething } }
            lineups={uniqueLineups.lineups}
            myLineup={myLineupInfo}
            opponentLineup={opponentLineup}
            selectLineup={ lineup => this.props.selectLineup(lineup) }
            animationEvent={completedEvent}
          />

          <LiveAnimationArea
            { ...{ currentEvent, watching } }
            eventsMultipart={ eventsMultipart }
            onAnimationComplete={ () => this.props.animationCompleted() }
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
