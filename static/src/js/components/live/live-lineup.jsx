import React from 'react';

import * as AppActions from '../../stores/app-state-store';
import LiveLineupPlayer from './live-lineup-player';
import LivePlayerPane from './live-player-pane';
import log from '../../lib/logging';


/**
 * Renders the lineup of players on the left/right hand side of the live section.
 */
const LiveLineup = React.createClass({

  propTypes: {
    changePathAndMode: React.PropTypes.func.isRequired,
    eventDescriptions: React.PropTypes.object.isRequired,
    games: React.PropTypes.object.isRequired,
    lineup: React.PropTypes.object.isRequired,
    mode: React.PropTypes.object.isRequired,
    playersPlaying: React.PropTypes.array.isRequired,
    relevantPlayerHistory: React.PropTypes.object.isRequired,
    whichSide: React.PropTypes.string.isRequired,
  },

  getInitialState() {
    return {
      // (optional) parameter assigned a player ID when we want to show their LivePlayerPane
      viewPlayerDetails: this.props.lineup.length > 0 ? this.props.lineup.roster[0] : undefined,
    };
  },

  /**
   * Used to close the current opponent lineup. Sets up parameters to then call props.changePathAndMode()
   */
  closeLineup() {
    const mode = this.props.mode;
    const path = `/live/lineups/${mode.myLineupId}/contests/${mode.contestId}`;
    const changedFields = {
      opponentLineupId: undefined,
    };

    this.props.changePathAndMode(path, changedFields);
  },

  /**
   * Action to open the player pane based on the state.viewPlayerDetails ID
   * Called when user clicks on a LiveLineupPlayer
   *
   * @param  {integer} Player ID to show the LivePlayerPane for
   */
  openPlayerPane(playerId) {
    log.debug('openPlayerPane() - open', playerId);

    this.setState({ viewPlayerDetails: playerId });
    if (this.props.whichSide === 'opponent') {
      AppActions.togglePlayerPane('right');
    } else {
      AppActions.togglePlayerPane('left');
    }
  },

  /**
   * Render the close lineup element
   *
   * @return {JSXElement}
   */
  renderCloseLineup() {
    // you cannot close your own lineup
    if (this.props.whichSide === 'mine') {
      return (<span />);
    }

    return (
      <span className="live-lineup__close" onClick={this.closeLineup}></span>
    );
  },

  /**
   * Renders the list of players
   *
   * @return {JSXElement}
   */
  renderPlayers() {
    const renderedPlayers = this.props.lineup.roster.map((playerId) => {
      const player = this.props.lineup.rosterDetails[playerId];
      const playerSRID = player.info.player_srid;
      const isPlaying = this.props.playersPlaying.indexOf(playerSRID) !== -1;
      const eventDescription = this.props.eventDescriptions[playerSRID] || undefined;

      return (
        <LiveLineupPlayer
          eventDescription={eventDescription}
          key={playerId}
          isPlaying={isPlaying}
          openPlayerPane={this.openPlayerPane.bind(this, playerId)}
          player={player}
          whichSide={this.props.whichSide}
        />
      );
    }, this);

    return (
      <ul className="live-lineup__players">
        {renderedPlayers}
      </ul>
    );
  },

  /**
   * Renders the LivePlayerPane for the user based on state.viewPlayerDetails
   *
   * @return {JSXElement}
   */
  renderPlayerPane() {
    const playerId = this.state.viewPlayerDetails;

    // don't show if there's no player or the player is not in the roster
    if (!playerId || this.props.lineup.roster.indexOf(playerId) === -1) {
      return ('');
    }

    const player = this.props.lineup.rosterDetails[playerId];
    const game = this.props.games[player.info.game_srid] || {};
    const history = this.props.relevantPlayerHistory[player.info.player_srid] || [];

    return (
      <LivePlayerPane
        whichSide={this.props.whichSide}
        player={player}
        eventHistory={history}
        game={game}
      />
    );
  },

  render() {
    // don't show until there's a roster
    if (this.props.lineup.roster.length === 0) {
      return (<div />);
    }

    const className = `cmp-live__lineup live-lineup live-lineup--${this.props.whichSide}`;

    return (
      <div className={className}>
        {this.renderCloseLineup()}
        {this.renderPlayers()}
        {this.renderPlayerPane()}
      </div>
    );
  },
});

export default LiveLineup;
