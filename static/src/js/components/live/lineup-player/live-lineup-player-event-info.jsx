import { humanizeFP } from '../../../lib/utils/numbers';
import React from 'react';

// assets
require('../../../../sass/blocks/live/lineup-player/live-lineup-player-event-info.scss');


/**
 * Stateless component that houses event description within a live lineup player
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
const LiveLineupPlayerEventInfo = (props) => {
  const { points = null, description, when } = props;
  const block = 'live-lineup-player-event-info';
  const pointsDom = (points !== null) ? (<div className={`${block}__points`}>{humanizeFP(points, true)}</div>) : '';

  return (
    <div className={block}>
      {pointsDom}
      <div className={`${block}__description`}>{description}</div>
      <div className={`${block}__when`}>{when.clock}</div>
    </div>
  );
};

LiveLineupPlayerEventInfo.propTypes = {
  description: React.PropTypes.string.isRequired,
  points: React.PropTypes.number,
  when: React.PropTypes.object.isRequired,
};

export default LiveLineupPlayerEventInfo;
