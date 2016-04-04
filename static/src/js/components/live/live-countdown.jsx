import React from 'react';
import CountdownClock from '../site/countdown-clock';


const LiveCountdown = React.createClass({

  propTypes: {
    lineup: React.PropTypes.object.isRequired,
    onCountdownComplete: React.PropTypes.func.isRequired,
  },

  render() {
    const { name, start } = this.props.lineup;
    const editLineup = `/draft/${ this.props.lineup.draftGroup.id }/lineup/${ this.props.lineup.id }/edit/`;

    return (
      <div className="live-countdown">
        <div className="live-countdown__lineup-name">{ name }</div>
        <div className="live-countdown__startsin">Starts in</div>
        <CountdownClock
          time={ new Date(start).getTime() }
          onCountdownOver={ this.props.onCountdownComplete }
        />
        <div className="live-countdown__actions">
          <a href={ editLineup } className="button--medium--outline">Edit Lineup</a>
          <a href="/lobby/" className="button--medium--outline">Enter Contests</a>
        </div>
      </div>
    );
  },
});

export default LiveCountdown;
