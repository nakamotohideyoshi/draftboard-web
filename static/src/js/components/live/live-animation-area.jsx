import { connect } from 'react-redux';
import React from 'react';
import LiveMLBStadium from './mlb/live-mlb-stadium';
import LiveNFLField from './nfl/live-nfl-field';
import LiveNBACourt from './live-nba-court';


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  animationEvent: state.events.animationEvent,
  eventsMultipart: state.eventsMultipart,
  watching: state.watching,
});

/**
 * Return the header section of the live page, including the lineup/contest title and overall stats
 */
export const LiveAnimationArea = (props) => {
  const { watching } = props;
  const { sport } = watching;
  const venues = [];

  switch (sport) {
    case 'mlb': {
      const { watchablePlayers, events } = props.eventsMultipart;
      const myEventId = watchablePlayers[watching.myPlayerSRID];
      const myEvent = events[myEventId] || {};
      let modifiers = ['all-mine'];

      if (watching.opponentLineupId) modifiers = ['splitscreen-mine'];
      venues.push(
        <LiveMLBStadium
          event={myEvent}
          key="mine"
          modifiers={modifiers}
          whichSide="mine"
        />
      );

      if (watching.opponentLineupId) {
        const opponentEventId = watchablePlayers[watching.opponentPlayerSRID];
        const opponentEvent = events[opponentEventId] || {};

        venues.push(
          <LiveMLBStadium
            event={opponentEvent}
            key="opponent"
            modifiers={['splitscreen-opponent']}
            whichSide="opponent"
          />
        );
      }

      break;
    }
    case 'nba':
      venues.push(
        <LiveNBACourt
          animationEvent={props.animationEvent}
          key="nba"
        />
      );
      break;
    case 'nfl':
      venues.push(
        <LiveNFLField
          animationEvent={props.animationEvent}
          key="nfl"
        />
      );
      break;
    default:
      break;
  }

  return (
    <div className={`live__venue-${sport}`}>
      {venues}
    </div>
  );
};

LiveAnimationArea.propTypes = {
  animationEvent: React.PropTypes.object,
  eventsMultipart: React.PropTypes.object.isRequired,
  watching: React.PropTypes.object.isRequired,
};

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  mapStateToProps
)(LiveAnimationArea);
