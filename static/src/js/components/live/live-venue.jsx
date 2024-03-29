import React from 'react';
import { get } from 'lodash';
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
      currentEvent: this.props.currentEvent || null,
      postPlayDescription: null,
    };
  },

  componentWillReceiveProps(nextProps) {
    this.setState({ currentEvent: nextProps.currentEvent });
  },

  stageAnimationStarted(animationCompletedPromise) {
    // Helper method for delaying callbacks within a promise chain.
    const wait = time => new Promise(resolve => setTimeout(resolve, time));

    animationCompletedPromise.then(() => {
      if (get(this.state.currentEvent, 'pbp.extra_info.touchdown', false)) {
        this.setState({ postPlayDescription: { title: 'Touchdown!' } });
        return wait(3000).then(
          () => this.setState({ postPlayDescription: null }
        ));
      }
      return this;
    }).then(
      () => this.setState({ currentEvent: null, postPlayDescription: null })
    ).then(
      () => wait(1000)
    ).then(
      () => (this.props.onAnimationCompleted ? this.props.onAnimationCompleted() : true)
    );
  },

  render() {
    return (
      <div>
        <section className="live__venues">
          <LiveHeader
            contest={this.props.contest}
            watching={this.props.watching}
            lineups={this.props.uniqueLineups.lineups}
            myLineup={this.props.myLineupInfo}
            opponentLineup={this.props.opponentLineup}
            message={ this.state.postPlayDescription || null }
          />

          {this.props.watching.sport === 'mlb' ? (
            <LiveMLBStage
              watching={this.props.watching}
              currentEvent={this.props.currentEvent}
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

          <LiveStandingsPane contest={this.props.contest} watching={this.props.watching} />
        </section>

        <LiveHistoryList currentEvent={this.props.currentEvent} />
      </div>
    );
  },
});
