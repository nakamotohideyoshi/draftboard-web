import React from 'react';
import LiveMLBStadium from './mlb/live-mlb-stadium';

export default React.createClass({

  propTypes: {
    currentEvent: React.PropTypes.object,
    eventsMultipart: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
    onAnimationStarted: React.PropTypes.func,
  },

  /**
   * Returns an array of MLB stadiums based on the lineups currently being watched.
   * @param  {object} props
   * @return {array}
   */
  renderMLBStadiums(props) {
    const { watching } = props;
    const { watchablePlayers, events } = props.eventsMultipart;
    const myEventId = watchablePlayers[watching.myPlayerSRID];
    const myEvent = events[myEventId] || {};
    const venues = [];
    const modifiers = watching.opponentLineupId ? ['splitscreen-mine'] : ['all-mine'];

    venues.push(<LiveMLBStadium event={myEvent} key="mine" modifiers={modifiers} whichSide="mine" />);

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

    return venues;
  },

  render() {
    return (
      <div className={`live__venue live__venue-${this.props.watching.sport}`}>
        { this.renderMLBStadiums(this.props) }
      </div>
    );
  },
});
