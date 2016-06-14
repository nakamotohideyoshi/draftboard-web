import React from 'react';
import CountdownClock from '../site/countdown-clock';


const LiveCountdown = (props) => (
  <div className="live-countdown">
    <div className="live-countdown__lineup-name">{props.entry.lineup_name}</div>
    <div className="live-countdown__startsin">Starts in</div>
    <CountdownClock time={props.entry.start} />
    <div className="live-countdown__actions">
      <a
        href={`/draft/${props.entry.draft_group}/lineup/${props.entry.lineup}/edit/`}
        className="button--medium--outline"
      >
        Edit Lineup
      </a>
      <a href="/lobby/" className="button--medium--outline">Enter Contests</a>
    </div>
  </div>
);

LiveCountdown.propTypes = {
  entry: React.PropTypes.object.isRequired,
};

export default LiveCountdown;
