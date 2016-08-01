import React from 'react';
import CountdownClock from '../site/countdown-clock';

// assets
require('../../../sass/blocks/live/live-countdown.scss');


/**
 * Stateless component that is a container around CountdownClock
 * - is stupid, so does not check if the lineup has already started
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
const LiveCountdown = (props) => {
  const block = 'live-countdown';

  return (
    <section className={block}>
      <div className={`${block}__lineup-name`}>{props.lineup.name}</div>
      <div className={`${block}__starts-in`}>Starts in</div>
      <CountdownClock
        modifiers={['live-countdown']}
        onCountdownOver={props.onCountdownOver}
        time={props.lineup.start}
      />
      <div className={`${block}__actions`}>
        <a
          href={`/draft/${props.lineup.draftGroup}/lineup/${props.lineup.id}/edit/`}
          className={`${block}__action`}
        >
          Edit Lineup
        </a>
        <a href="/contests/" className={`${block}__action`}>Enter Contests</a>
      </div>
    </section>
  );
};

LiveCountdown.propTypes = {
  lineup: React.PropTypes.object.isRequired,
  onCountdownOver: React.PropTypes.func,
};

export default LiveCountdown;
