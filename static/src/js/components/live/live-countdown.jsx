import React from 'react';
import CountdownClock from '../site/countdown-clock';


const LiveCountdown = (props) => (
  <div className="live-countdown">
    <div className="live-countdown__lineup-name">{props.lineup.name}</div>
    <div className="live-countdown__startsin">Starts in</div>
    <CountdownClock
      onCountdownOver={props.onCountdownOver}
      time={props.lineup.start}
    />
    <div className="live-countdown__actions">
      <a
        href={`/draft/${props.lineup.draft_group}/lineup/${props.lineup.id}/edit/`}
        className="button--medium--outline"
      >
        Edit Lineup
      </a>
      <a href="/lobby/" className="button--medium--outline">Enter Contests</a>
    </div>
  </div>
);

LiveCountdown.propTypes = {
  lineup: React.PropTypes.object.isRequired,
  onCountdownOver: React.PropTypes.func,
};

export default LiveCountdown;
