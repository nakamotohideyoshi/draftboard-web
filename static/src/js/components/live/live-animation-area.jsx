import React from 'react';
import LiveMLBStadium from './mlb/live-mlb-stadium';
import LiveAnimationStage from './live-animation-stage';

export default React.createClass({

  propTypes: {
    currentEvent: React.PropTypes.object,
    eventsMultipart: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
    onAnimationComplete: React.PropTypes.func,
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

  /**
   * Renders a NBACourt component.
   * @return {object} LiveNBACourt
   */
  renderStage(sport) {
    if (sport === 'mlb') {
      return this.renderMLBStadiums(this.props);
    }

    return (
      <LiveAnimationStage
        key={`${sport}-stage`}
        sport={sport}
        onAnimationComplete={(event) => this.props.onAnimationComplete(event)}
        currentEvent={this.props.currentEvent}
      />
    );
  },

  render() {
    return (
      <div className={`live__venue live__venue-${this.props.watching.sport}`}>
        { this.renderStage(this.props.watching.sport) }
      </div>
    );
  },
});
