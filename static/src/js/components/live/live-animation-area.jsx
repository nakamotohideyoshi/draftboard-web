import React from 'react';
import LiveMLBStadium from './mlb/live-mlb-stadium';
import LiveNFLField from './nfl/live-nfl-field';
import LiveNBACourt from './nba/live-nba-court';

export default React.createClass({

  propTypes: {
    animationEvent: React.PropTypes.object,
    eventsMultipart: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  /**
   * Returns an array of MLB venues.
   * @param  {object} props
   * @return {array}
   */
  getMLBVenues() {
    const { watching } = this.props;
    const { watchablePlayers, events } = this.props.eventsMultipart;
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

  renderVenues() {
    switch (this.props.watching.sport) {
      case 'mlb':
        return this.getMLBVenues(this.props);
      case 'nba':
        return <LiveNBACourt key="nba" animationEvent={this.props.animationEvent} />;
      case 'nfl':
        return <LiveNFLField key="nfl" animationEvent={this.props.animationEvent} />;
      default:
        return [];
    }
  },

  render() {
    return (
      <div className={`live__venue live__venue-${this.props.watching.sport}`}>
        { this.renderVenues() }
      </div>
    );
  },
});
