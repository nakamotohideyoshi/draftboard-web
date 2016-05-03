import * as AppActions from '../../stores/app-state-store';
import * as ReactRedux from 'react-redux';
import LiveLineupPlayer from './live-lineup-player';
import LivePlayerPane from './live-player-pane';
import log from '../../lib/logging';
import React from 'react';
import size from 'lodash/size';
import {
  relevantPlayerBoxScoreHistoriesSelector,
  relevantPlayerTeamsSelector,
  relevantPlayersSelector,
} from '../../selectors/live-players';
import { sportsSelector } from '../../selectors/sports';


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  playerEventDescriptions: state.events.playerEventDescriptions,
  playerHistories: state.events.playerHistories,
  playersPlaying: state.events.playersPlaying,
  relevantPlayerTeamsSelector: relevantPlayerTeamsSelector(state),
  relevantSeasonStats: relevantPlayerBoxScoreHistoriesSelector(state),
  relevantPlayersGameStats: relevantPlayersSelector(state),
  sports: sportsSelector(state),
});

/**
 * Renders the lineup of players on the left/right hand side of the live section.
 */
const LiveLineup = React.createClass({

  propTypes: {
    changePathAndMode: React.PropTypes.func.isRequired,
    draftGroupStarted: React.PropTypes.bool.isRequired,
    lineup: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
    playerEventDescriptions: React.PropTypes.object.isRequired,
    playersPlaying: React.PropTypes.array.isRequired,
    playerHistories: React.PropTypes.object.isRequired,
    relevantPlayersGameStats: React.PropTypes.object.isRequired,
    relevantPlayerTeamsSelector: React.PropTypes.object.isRequired,
    relevantSeasonStats: React.PropTypes.object.isRequired,
    sports: React.PropTypes.object.isRequired,
    watchingPlayerSRID: React.PropTypes.string,
    whichSide: React.PropTypes.string.isRequired,
  },

  getInitialState() {
    return {
      // (optional) parameter assigned a player ID when we want to show their LivePlayerPane
      viewPlayerDetails: size(this.props.lineup) > 0 ? this.props.lineup.roster[0] : undefined,
    };
  },

  /**
   * Used to close the current opponent lineup. Sets up parameters to then call props.changePathAndMode()
   */
  closeLineup() {
    const watching = this.props.watching;
    const path = `/live/${watching.sport}/lineups/${watching.myLineupId}/contests/${watching.contestId}`;
    const changedFields = {
      opponentLineupId: null,
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
      const playerSRID = player.srid;
      const isPlaying = this.props.playersPlaying.indexOf(playerSRID) !== -1;
      const isWatching = this.props.watchingPlayerSRID === playerSRID;
      const eventDescription = this.props.playerEventDescriptions[playerSRID] || {};
      const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${this.props.watching.sport}/120`;
      const gameStats = this.props.relevantPlayersGameStats[playerSRID] || {};

      return (
        <LiveLineupPlayer
          draftGroupStarted={this.props.draftGroupStarted}
          eventDescription={eventDescription}
          key={playerId}
          isPlaying={isPlaying}
          isWatching={isWatching}
          openPlayerPane={this.openPlayerPane.bind(this, playerId)}
          player={player}
          playerImagesBaseUrl={playerImagesBaseUrl}
          gameStats={gameStats}
          sport={this.props.watching.sport}
          whichSide={this.props.whichSide}
        />
      );
    }, this);

    return (
      <div className="live-lineup__players">
        {this.renderCloseLineup()}
        <ul>
          {renderedPlayers}
        </ul>
      </div>
    );
  },

  /**
   * Renders the LivePlayerPane for the user based on state.viewPlayerDetails
   *
   * @return {JSXElement}
   */
  renderPlayerPane() {
    // don't show player pane while countdown is showing
    if (!this.props.draftGroupStarted) return '';

    const { lineup } = this.props;
    const playerId = this.state.viewPlayerDetails;

    // don't show if there's no player or the player is not in the roster
    if (!playerId || lineup.roster.indexOf(playerId) === -1) {
      return ('');
    }

    const player = lineup.rosterDetails[playerId];
    const game = this.props.sports.games[player.gameSRID] || {};
    const history = this.props.playerHistories[player.srid] || [];

    return (
      <LivePlayerPane
        eventHistory={history}
        game={game}
        seasonStats={this.props.relevantSeasonStats[player.srid] || {}}
        player={player}
        playerImagesBaseUrl={`${window.dfs.playerImagesBaseUrl}/${this.props.watching.sport}/380`}
        playerTeam={relevantPlayerTeamsSelector[playerId] || {}}
        sport={this.props.watching.sport}
        whichSide={this.props.whichSide}
      />
    );
  },

  render() {
    // don't show until there's a roster
    if (this.props.lineup.hasOwnProperty('roster') === false || this.props.lineup.roster.length === 0) {
      return (<div />);
    }

    const className = `cmp-live__lineup live-lineup live-lineup--${this.props.whichSide}`;

    return (
      <div className={className}>
        {this.renderPlayers()}
        {this.renderPlayerPane()}
      </div>
    );
  },
});

// Set up Redux connections to React
const { connect } = ReactRedux;

// Wrap the component to inject dispatch and selected state into it.
const LiveLineupConnected = connect(
  mapStateToProps
)(LiveLineup);

export default LiveLineupConnected;
