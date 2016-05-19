import React from 'react';
import LiveMLBPitchZone from './live-mlb-pitch-zone';


/**
 * The court in the middle of the page
 */
const LiveMLBStadium = (props) => {
  let renderPitchZones = [];
  const { watching } = props;

  if (watching.myLineupId) {
    let event = {};

    if (watching.myPlayerSRID) {
      const { eventsMultipart } = props;
      const eventId = eventsMultipart.watchablePlayers[watching.myPlayerSRID];
      event = eventsMultipart.events[eventId] || {};
    }

    const pitchZoneBlock = (<LiveMLBPitchZone key="0" event={event} whichSide="mine" />);

    if (watching.opponentLineupId) {
      renderPitchZones.push(
        <div key="2" className="live-mlb-stadium__splitscreen--mine">
          <img src="/static/src/img/blocks/live/bg-mlb.jpg" alt="Baseball Background" />
          {pitchZoneBlock}
        </div>
      );
    } else {
      renderPitchZones.push(pitchZoneBlock);
    }
  }

  if (watching.opponentLineupId) {
    let event = {};

    if (watching.opponentPlayerSRID) {
      const { eventsMultipart } = props;
      const eventId = eventsMultipart.watchablePlayers[watching.opponentPlayerSRID];
      event = eventsMultipart.events[eventId];
    }

    // note that the img tag is required to make the background be positioned absolutely
    renderPitchZones.push(
      <div key="3" className="live-mlb-stadium__splitscreen--opponent">
        <img src="/static/src/img/blocks/live/bg-mlb.jpg" alt="Baseball Background" />
        <LiveMLBPitchZone key="1" event={event} whichSide="opponent" />
      </div>
    );
  }

  return (
    <section className="cmp-live__mlb-stadium live-mlb-stadium">
      <div className="pitch-zone-filler" />
      {renderPitchZones}
    </section>
  );
};

LiveMLBStadium.propTypes = {
  animationEvents: React.PropTypes.object.isRequired,
  eventsMultipart: React.PropTypes.object.isRequired,
  watching: React.PropTypes.object.isRequired,
};

export default LiveMLBStadium;
