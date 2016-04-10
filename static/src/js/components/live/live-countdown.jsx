import React from 'react';
import CountdownClock from '../site/countdown-clock';


const LiveCountdown = (props) => {
  const { name, start } = props.lineup;
  const editLineup = `/draft/${props.lineup.draftGroup.id}/lineup/${props.lineup.id}/edit/`;

  return (
    <div className="live-countdown">
      <div className="live-countdown__lineup-name">{ name }</div>
      <div className="live-countdown__startsin">Starts in</div>
      <CountdownClock
        time={ new Date(start).getTime() }
        onCountdownOver={ props.onCountdownComplete }
      />
      <div className="live-countdown__actions">
        <a href={ editLineup } className="button--medium--outline">Edit Lineup</a>
        <a href="/lobby/" className="button--medium--outline">Enter Contests</a>
      </div>
    </div>
  );
};

LiveCountdown.propTypes = {
  lineup: React.PropTypes.object.isRequired,
  onCountdownComplete: React.PropTypes.func.isRequired,
};

export default LiveCountdown;
