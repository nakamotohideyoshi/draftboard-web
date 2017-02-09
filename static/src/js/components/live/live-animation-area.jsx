import React from 'react';
import LiveMLBStadium from './mlb/live-mlb-stadium';
import LiveNFLField from './nfl/live-nfl-field';
import LiveNBACourt from './nba/live-nba-court';
import {
  clearCurrentEvent,
  shiftOldestEvent,
  showAnimationEventResults,
} from '../../actions/events';
import store from '../../store';

export default React.createClass({

  propTypes: {
    currentEvent: React.PropTypes.object,
    eventsMultipart: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  /**
   * Handler for when a venue's animation has completed.
   */
  nbaAnimationCompleted() {
    // show the results, remove the animation
    store.dispatch(showAnimationEventResults(this.props.currentEvent));

    // remove the event
    store.dispatch(clearCurrentEvent());

    // enter the next item in the queue once everything is done.
    setTimeout(() => {
      store.dispatch(shiftOldestEvent());
    }, 1000);
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
  renderNBACourt() {
    return (
      <LiveNBACourt
        key="nba-court"
        onAnimationComplete={() => this.nbaAnimationCompleted()}
        currentEvent={this.props.currentEvent}
      />
    );
  },

  /**
   * Renders the venue DOM for a given sport.
   * @return {object} Sport specific DOM.
   */
  renderVenue(sport) {
    switch (sport) {
      case 'mlb':
        return this.renderMLBStadiums(this.props);
      case 'nba':
        return this.renderNBACourt();
      case 'nfl':
        return <LiveNFLField key="nfl" currentEvent={this.props.currentEvent} />;
      default:
        return [];
    }
  },

  render() {
    return (
      <div className={`live__venue live__venue-${this.props.watching.sport}`}>
        { this.renderVenue(this.props.watching.sport) }
      </div>
    );
  },
});
